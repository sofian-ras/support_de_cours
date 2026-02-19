import pandas as pd
from itemadapter import ItemAdapter

class CleaningPipeline:
    """Nettoie les données"""
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Nettoyer titre
        if adapter.get('title'):
            adapter['title'] = adapter['title'].strip()
        
        # Nettoyer description
        if adapter.get('description'):
            adapter['description'] = adapter['description'].replace('\n', ' ').strip()
        
        return item

class ExcelExportPipeline:
    """Export vers Excel"""
    def open_spider(self, spider):
        self.books = []
    
    def close_spider(self, spider):
        if self.books:
            df = pd.DataFrame(self.books)
            
            # Statistiques par catégorie
            cat_stats = df.groupby('category').agg({
                'title': 'count',
                'price': 'mean'
            }).reset_index()
            cat_stats.columns = ['category', 'book_count', 'avg_price']
            
            # Sauvegarder Excel
            with pd.ExcelWriter('data/books_complet.xlsx', engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Livres', index=False)
                cat_stats.to_excel(writer, sheet_name='Catégories', index=False)
            
            spider.logger.info(f" Export Excel : {len(df)} livres")
    
    def process_item(self, item, spider):
        self.books.append(ItemAdapter(item).asdict())
        return item