from django.test import TestCase
from django.contrib.gis.geos import fromstr
from core.models import Dataset, AOI, Label, Model, Training, Feedback, FeedbackAOI, FeedbackLabel
from login.models import OsmUser

class DatasetModelTest(TestCase):
    def setUp(self):
        self.user = OsmUser.objects.create(osm_id='123456789')
        self.dataset = Dataset.objects.create(name="Sample Dataset", created_by=self.user)

    def test_dataset_creation(self):
        expected_str = f'Dataset object ({self.dataset.id})'
        self.assertEqual(str(self.dataset), expected_str)

class AOIModelTest(TestCase):
    def setUp(self):
        self.user = OsmUser.objects.create(osm_id='987654321')
        self.dataset = Dataset.objects.create(name="Sample Dataset", created_by=self.user)
        self.aoi = AOI.objects.create(dataset=self.dataset, geom=fromstr('POLYGON((0 0, 1 1, 1 0, 0 0))'))

    def test_aoi_creation(self):
        self.assertTrue(isinstance(self.aoi, AOI))
        self.assertEqual(self.aoi.dataset, self.dataset)

class LabelModelTest(TestCase):
    def setUp(self):
        self.user = OsmUser.objects.create(osm_id='123456789')
        self.dataset = Dataset.objects.create(name="Sample Dataset", created_by=self.user)
        self.aoi = AOI.objects.create(dataset=self.dataset, geom=fromstr('POLYGON((0 0, 1 1, 1 0, 0 0))'))
        self.label = Label.objects.create(aoi=self.aoi, geom=fromstr('POINT(0 0)'))

    def test_label_creation(self):
        self.assertTrue(isinstance(self.label, Label))
        self.assertEqual(self.label.aoi, self.aoi)

class ModelModelTest(TestCase):
    def setUp(self):
        self.user = OsmUser.objects.create(osm_id='987654321')
        self.dataset = Dataset.objects.create(name="Sample Dataset", created_by=self.user)
        self.model = Model.objects.create(name="Sample Model", created_by=self.user, dataset=self.dataset)

    def test_model_creation(self):
        self.assertTrue(isinstance(self.model, Model))
        self.assertEqual(self.model.name, "Sample Model")

class TrainingModelTest(TestCase):
    def setUp(self):
        self.user = OsmUser.objects.create(osm_id='123456789')
        self.dataset = Dataset.objects.create(name="Sample Dataset", created_by=self.user)
        self.model_instance = Model.objects.create(name="Sample Model", created_by=self.user, dataset=self.dataset)
        self.training = Training.objects.create(
            model=self.model_instance, 
            created_by=self.user, 
            epochs=10, 
            batch_size=5, 
            zoom_level=[10, 12, 14, 16]
        )

    def test_training_creation(self):
        self.assertTrue(isinstance(self.training, Training))
        self.assertEqual(self.training.model, self.model_instance)

class FeedbackModelTest(TestCase):
    def setUp(self):
        self.user = OsmUser.objects.create(osm_id='987654321')
        self.dataset = Dataset.objects.create(name="Sample Dataset", created_by=self.user)
        self.model_instance = Model.objects.create(name="Sample Model", created_by=self.user, dataset=self.dataset)
        self.training = Training.objects.create(
            model=self.model_instance, 
            created_by=self.user, 
            epochs=5, 
            batch_size=10, 
            zoom_level=[10, 12, 14, 16]
        )
        self.feedback = Feedback.objects.create(
            training=self.training,
            user=self.user,
            geom=fromstr('POINT(0 0)'),
            feedback_type='TP',
            zoom_level=20
        )

    def test_feedback_creation(self):
        self.assertTrue(isinstance(self.feedback, Feedback))
        self.assertEqual(self.feedback.training, self.training)


class FeedbackLabelModelTest(TestCase):
    def setUp(self):
        self.user = OsmUser.objects.create(osm_id='987654321')
        self.dataset = Dataset.objects.create(name="Sample Dataset", created_by=self.user)
        self.model_instance = Model.objects.create(name="Sample Model", created_by=self.user, dataset=self.dataset)
        self.training = Training.objects.create(
            model=self.model_instance, 
            created_by=self.user, 
            epochs=5, 
            batch_size=10, 
            zoom_level=[10, 12, 14, 16]  # Example values
        )
        self.feedback_aoi = FeedbackAOI.objects.create(
            training=self.training,
            geom=fromstr('POLYGON((0 0, 1 1, 1 0, 0 0))'),  # Example Polygon geometry
            user=self.user
        )
        self.feedback_label = FeedbackLabel.objects.create(
            feedback_aoi=self.feedback_aoi,
            geom=fromstr('POLYGON((0.1 0.1, 0.9 0.9, 0.9 0.1, 0.1 0.1))'),  # Example smaller Polygon within the AOI
            osm_id=123456789
        )

    def test_feedback_label_creation(self):
        self.assertTrue(isinstance(self.feedback_label, FeedbackLabel))
        self.assertEqual(self.feedback_label.feedback_aoi, self.feedback_aoi)
