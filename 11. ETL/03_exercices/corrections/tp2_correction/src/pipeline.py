import pandas as pd
import requests
from datetime import datetime
from src.extractors.extractors import CSVExtractor, APIExtractor
from src.transformers.cleaner import DataTransformer
from src.loaders.loader import DataLoader


class SalesPipeline:
    """Pipeline ETL pour les ventes"""
    
    def __init__(self,config,logger):
        self.config = config
        self.logger = logger
        self.transformer = DataTransformer(logger)
        self.loader = DataLoader(logger)

        # Extractors
        self.csv_extractor = CSVExtractor(logger)
        self.weather_extractor = APIExtractor(logger,config['api_base_url'])

        # Data
        self.ventes_df = None
        self.produits_df = None
        self.meteo = None

    def run(self):
        """Exécute le pipeline"""
        try:
            self.logger.info("="*60)
            self.logger.info(f"DÉBUT DU PIPELINE - {datetime.now()}")
            self.logger.info("="*60)
            
            # Extract
            self._extract()
            
            # Transform
            self._transform()
            
            # Load
            self._load()
            
            self.logger.info("\n" + "="*60)
            self.logger.info("PIPELINE TERMINÉ AVEC SUCCÈS")
            self.logger.info("="*60)
            
        except Exception as e:
            self.logger.error(f"\nERREUR PIPELINE: {e}")
            raise

    def _extract(self):
        """Extraction des données"""
        self.logger.info("\n[1/3] === EXTRACTION ===")

        # 1. CSV ventes
        self.ventes_df = self.csv_extractor.extract(self.config['csv_path'])

        # 2. Produits (simulation avec données locales)
        self.logger.info("Chargement catalogue produits")
        produits_data = [
            {'produit_id': 1, 'nom': 'Souris', 'categorie': 'Périphérique', 'fournisseur': 'TechCo'},
            {'produit_id': 2, 'nom': 'Clavier', 'categorie': 'Périphérique', 'fournisseur': 'TechCo'},
            {'produit_id': 3, 'nom': 'Câble USB', 'categorie': 'Accessoire', 'fournisseur': 'AccessPlus'},
            {'produit_id': 4, 'nom': 'Webcam', 'categorie': 'Périphérique', 'fournisseur': 'VisionTech'},
            {'produit_id': 5, 'nom': 'Casque', 'categorie': 'Audio', 'fournisseur': 'SoundPro'},
        ]
        self.produits_df = pd.DataFrame(produits_data)

        # 3. Météo
        try:
            api_key = self.config.get('weather_api_key')
            if api_key:
                params = {'q': 'Paris', 'appid': api_key, 'units': 'metric', 'lang': 'fr'}
                data = self.weather_extractor.extract("weather", params=params)
                
                self.meteo = {
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description']
                }
                self.logger.info(f"Météo récupérée: {self.meteo['temperature']}°C, {self.meteo['description']}")
            else:
                self.logger.warning("Pas de clé API météo fournie")
                self.meteo = {"temperature": None, "description": "N/A"}
        except Exception as e:
            self.logger.warning(f"Météo non disponible: {e}")
            self.meteo = {'temperature': None, 'description': 'N/A'}


    def _transform(self):
        """Transformation des données"""
        self.logger.info("\n[2/3] === TRANSFORMATION ===")
        
        # Nettoyage
        self.ventes_df = self.transformer.clean(self.ventes_df)
        
        # Conversion date
        self.ventes_df['date'] = pd.to_datetime(self.ventes_df['date'])
        
        # Calcul montant_total
        self.ventes_df['montant_total'] = (
            self.ventes_df['quantite'] * self.ventes_df['prix_unitaire']
        )
        self.logger.info("Montant total calculé")
        
        # Enrichissement avec infos produits
        self.ventes_df = self.ventes_df.merge(
            self.produits_df,
            on='produit_id',
            how='left'
        )
        self.logger.info("Données enrichies avec catalogue produits")
        
        # Agrégations
        self.par_produit = self.ventes_df.groupby(['produit_id', 'nom', 'categorie']).agg({
            'quantite': 'sum',
            'montant_total': 'sum'
        }).reset_index()
        self.par_produit = self.par_produit.sort_values('montant_total', ascending=False)

        # Agrégation par catégorie
        par_categorie = self.ventes_df.groupby('categorie').agg({
            'quantite': 'sum',
            'montant_total': ['sum', 'mean', 'count']
        }).reset_index()

        # Aplatir les colonnes MultiIndex en noms simples
        par_categorie.columns = [
            'categorie',
            'quantite_totale',
            'montant_total',
            'montant_moyen',
            'nb_transactions'
        ]

        self.par_categorie = par_categorie

        self.logger.info("Agrégations calculées")

    def _load(self):
        """Chargement des données"""
        self.logger.info("\n[3/3] === CHARGEMENT ===")
        
        # Préparer métadonnées
        metadata = pd.DataFrame([{
            'date_execution': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'nb_transactions': len(self.ventes_df),
            'montant_total': self.ventes_df['montant_total'].sum(),
            'temperature': self.meteo['temperature'],
            'meteo_description': self.meteo['description']
        }])
        
        # Charger vers Excel
        dataframes = {
            'Ventes détaillées': self.ventes_df,
            'Par produit': self.par_produit,
            'Par catégorie': self.par_categorie,
            'Métadonnées': metadata
        }
        
        self.loader.load_multiple_sheets(dataframes, self.config['output_path'])
        
        # Aussi en CSV pour archivage
        output_csv = self.config['output_path'].replace('.xlsx', '.csv')
        self.loader.load_csv(self.ventes_df, output_csv)
        
        self.logger.info(f"\nStatistiques:")
        self.logger.info(f"  - Transactions: {len(self.ventes_df)}")
        self.logger.info(f"  - Produits uniques: {self.ventes_df['produit_id'].nunique()}")
        self.logger.info(f"  - Montant total: {self.ventes_df['montant_total'].sum():.2f}€")
        self.logger.info(f"  - Catégorie top: {self.par_categorie.iloc[0]['categorie']}")
