import pytest
import json
import numpy as np
from unittest.mock import Mock, patch
from app_satisfaction import app, prediction_history


@pytest.fixture
def client():
    """Fixture pour créer un client de test Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_model():
    """Fixture pour créer un modèle mockup"""
    model = Mock()
    # Le modèle retourne toujours 7.5 pour les prédictions
    model.predict.return_value = np.array([7.5])
    return model


@pytest.fixture(autouse=True)
def clear_history():
    """Fixture pour nettoyer l'historique avant chaque test"""
    prediction_history.clear()
    yield
    prediction_history.clear()


class TestHealthEndpoint:
    """Tests pour l'endpoint /health"""

    def test_health_endpoint_returns_200(self, client):
        """Test que l'endpoint health retourne 200"""
        response = client.get('/health')
        assert response.status_code == 200

    def test_health_endpoint_returns_json(self, client):
        """Test que l'endpoint health retourne du JSON"""
        response = client.get('/health')
        assert response.content_type == 'application/json'

    def test_health_endpoint_has_status_ok(self, client):
        """Test que l'endpoint health contient status: ok"""
        response = client.get('/health')
        data = json.loads(response.data)
        assert data['status'] == 'ok'

    def test_health_endpoint_has_model_loaded(self, client):
        """Test que l'endpoint health indique si le modèle est chargé"""
        response = client.get('/health')
        data = json.loads(response.data)
        assert 'model_loaded' in data
        assert isinstance(data['model_loaded'], bool)

    def test_health_endpoint_has_timestamp(self, client):
        """Test que l'endpoint health contient un timestamp"""
        response = client.get('/health')
        data = json.loads(response.data)
        assert 'timestamp' in data
        assert isinstance(data['timestamp'], str)


class TestPredictEndpoint:
    """Tests pour l'endpoint /predict"""

    # def test_predict_endpoint_returns_200(self, client, mock_model):
    #     """Test que l'endpoint predict retourne 200 avec des données valides"""
    #     response = client.post('/predict',
    #                           data=json.dumps({'features': [30, 12, 15, 2]}),
    #                           content_type='application/json')
    #     assert response.status_code == 200

    # def test_predict_endpoint_returns_satisfaction(self, client, mock_model):
    #     """Test que l'endpoint predict retourne une satisfaction"""
    #     response = client.post('/predict',
    #                           data=json.dumps({'features': [30, 12, 15, 2]}),
    #                           content_type='application/json')
    #     data = json.loads(response.data)
    #     assert 'satisfaction' in data
    #     assert isinstance(data['satisfaction'], (int, float))

    # def test_predict_endpoint_returns_timestamp(self, client, mock_model):
    #     """Test que l'endpoint predict retourne un timestamp"""
    #     response = client.post('/predict',
    #                           data=json.dumps({'features': [30, 12, 15, 2]}),
    #                           content_type='application/json')
    #     data = json.loads(response.data)
    #     assert 'timestamp' in data
    #     assert isinstance(data['timestamp'], str)

    def test_predict_missing_features_returns_400(self, client, mock_model):
        """Test que l'absence du champ features retourne 400"""
        response = client.post('/predict',
                              data=json.dumps({}),
                              content_type='application/json')
        assert response.status_code == 400

    def test_predict_wrong_number_of_features_returns_400(self, client, mock_model):
        """Test qu'un nombre incorrect de features retourne 400"""
        response = client.post('/predict',
                              data=json.dumps({'features': [30, 12]}),
                              content_type='application/json')
        assert response.status_code == 400

    def test_predict_non_numeric_features_returns_400(self, client,mock_model):
        """Test que des features non numériques retournent 400"""
        response = client.post('/predict',
                              data=json.dumps({'features': ['age', 12, 15, 2]}),
                              content_type='application/json')
        assert response.status_code == 400

    def test_predict_features_not_list_returns_400(self, client, mock_model):
        """Test que features doit être une liste"""
        response = client.post('/predict',
                              data=json.dumps({'features': 'invalid'}),
                              content_type='application/json')
        assert response.status_code == 400

    def test_predict_no_model_returns_500(self, client):
        """Test que l'absence de modèle retourne 500"""
        response = client.post('/predict',
                              data=json.dumps({'features': [30, 12, 15, 2]}),
                              content_type='application/json')
        assert response.status_code == 500


class TestBatchPredictEndpoint:
    """Tests pour l'endpoint /batch_predict"""

    @patch('app_satisfaction.model')
    def test_batch_predict_returns_200(self, mock_model_patch, client):
        """Test que l'endpoint batch_predict retourne 200"""
        mock_model_patch.predict.return_value = np.array([7.5, 6.2])

        response = client.post('/batch_predict',
                              data=json.dumps({
                                  'features_list': [
                                      [30, 12, 15, 2],
                                      [45, 24, 30, 5]
                                  ]
                              }),
                              content_type='application/json')
        assert response.status_code == 200

    @patch('app_satisfaction.model')
    def test_batch_predict_returns_satisfactions_list(self, mock_model_patch, client):
        """Test que l'endpoint batch_predict retourne une liste de satisfactions"""
        mock_model_patch.predict.return_value = np.array([7.5, 6.2])

        response = client.post('/batch_predict',
                              data=json.dumps({
                                  'features_list': [
                                      [30, 12, 15, 2],
                                      [45, 24, 30, 5]
                                  ]
                              }),
                              content_type='application/json')
        data = json.loads(response.data)
        assert 'satisfactions' in data
        assert isinstance(data['satisfactions'], list)
        assert len(data['satisfactions']) == 2

    @patch('app_satisfaction.model')
    def test_batch_predict_returns_count(self, mock_model_patch, client):
        """Test que l'endpoint batch_predict retourne le nombre de prédictions"""
        mock_model_patch.predict.return_value = np.array([7.5, 6.2])

        response = client.post('/batch_predict',
                              data=json.dumps({
                                  'features_list': [
                                      [30, 12, 15, 2],
                                      [45, 24, 30, 5]
                                  ]
                              }),
                              content_type='application/json')
        data = json.loads(response.data)
        assert 'count' in data
        assert data['count'] == 2

    def test_batch_predict_missing_features_list_returns_400(self, client):
        """Test que l'absence du champ features_list retourne 400"""
        response = client.post('/batch_predict',
                              data=json.dumps({}),
                              content_type='application/json')
        assert response.status_code == 400

    def test_batch_predict_empty_list_returns_400(self, client):
        """Test qu'une liste vide retourne 400"""
        response = client.post('/batch_predict',
                              data=json.dumps({'features_list': []}),
                              content_type='application/json')
        assert response.status_code == 400

    def test_batch_predict_invalid_entry_returns_400(self, client):
        """Test qu'une entrée invalide retourne 400"""
        response = client.post('/batch_predict',
                              data=json.dumps({
                                  'features_list': [
                                      [30, 12, 15, 2],
                                      [45, 24]  # Nombre incorrect de features
                                  ]
                              }),
                              content_type='application/json')
        assert response.status_code == 400

    @patch('app_satisfaction.model', None)
    def test_batch_predict_no_model_returns_500(self, client):
        """Test que l'absence de modèle retourne 500"""
        response = client.post('/batch_predict',
                              data=json.dumps({
                                  'features_list': [[30, 12, 15, 2]]
                              }),
                              content_type='application/json')
        assert response.status_code == 500


class TestHistoryEndpoint:
    """Tests pour l'endpoint /history"""

    def test_history_endpoint_returns_200(self, client):
        """Test que l'endpoint history retourne 200"""
        response = client.get('/history')
        assert response.status_code == 200

    def test_history_endpoint_returns_empty_list_initially(self, client):
        """Test que l'historique est vide initialement"""
        response = client.get('/history')
        data = json.loads(response.data)
        assert 'history' in data
        assert data['history'] == []
        assert data['total'] == 0

    @patch('app_satisfaction.model')
    def test_history_contains_predictions(self, mock_model_patch, client):
        """Test que l'historique contient les prédictions"""
        mock_model_patch.predict.return_value = np.array([7.5])

        # Faire une prédiction
        client.post('/predict',
                   data=json.dumps({'features': [30, 12, 15, 2]}),
                   content_type='application/json')

        # Vérifier l'historique
        response = client.get('/history')
        data = json.loads(response.data)
        assert len(data['history']) == 1
        assert data['total'] == 1

    def test_history_respects_limit(self, client):
        """Test que l'endpoint history respecte le paramètre limit"""
        # Ajouter plusieurs entrées manuellement
        from app_satisfaction import prediction_history
        for i in range(20):
            prediction_history.append({
                'timestamp': '2024-01-01',
                'features': [30, 12, 15, 2],
                'satisfaction': 7.5,
                'type': 'single'
            })

        response = client.get('/history?limit=5')
        data = json.loads(response.data)
        assert data['returned'] == 5
        assert data['total'] == 20

    def test_history_limit_too_small_returns_400(self, client):
        """Test qu'une limite trop petite retourne 400"""
        response = client.get('/history?limit=0')
        assert response.status_code == 400

    def test_history_limit_too_large_returns_400(self, client):
        """Test qu'une limite trop grande retourne 400"""
        response = client.get('/history?limit=101')
        assert response.status_code == 400

    def test_history_default_limit_is_10(self, client):
        """Test que la limite par défaut est 10"""
        from app_satisfaction import prediction_history
        for i in range(20):
            prediction_history.append({
                'timestamp': '2024-01-01',
                'features': [30, 12, 15, 2],
                'satisfaction': 7.5,
                'type': 'single'
            })

        response = client.get('/history')
        data = json.loads(response.data)
        assert data['returned'] == 10


class TestStatsEndpoint:
    """Tests pour l'endpoint /stats"""

    def test_stats_endpoint_returns_200(self, client):
        """Test que l'endpoint stats retourne 200"""
        response = client.get('/stats')
        assert response.status_code == 200

    def test_stats_empty_history(self, client):
        """Test des stats avec un historique vide"""
        response = client.get('/stats')
        data = json.loads(response.data)
        assert data['total_predictions'] == 0

    @patch('app_satisfaction.model')
    def test_stats_with_predictions(self, mock_model_patch, client):
        """Test des stats avec des prédictions"""
        mock_model_patch.predict.return_value = np.array([7.5])

        # Faire plusieurs prédictions
        for _ in range(3):
            client.post('/predict',
                       data=json.dumps({'features': [30, 12, 15, 2]}),
                       content_type='application/json')

        response = client.get('/stats')
        data = json.loads(response.data)

        assert data['total_predictions'] == 3
        assert 'average_satisfaction' in data
        assert 'min_satisfaction' in data
        assert 'max_satisfaction' in data
        assert 'std_satisfaction' in data
