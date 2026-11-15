"""ML-specific tests: MODEL TRAINING behaviour."""

import numpy as np
import pytest

from ecom.config import MIN_ACCURACY, MIN_F1, TARGET
from ecom.features import build_features
from ecom.metrics import evaluate_model
from ecom.train import ModelTrainer


@pytest.fixture(scope="module")
def training_data():
    from ecom.data_ingestion import SessionDataGenerator

    df = SessionDataGenerator(seed=11).generate(1500)
    return build_features(df), df[TARGET]


def test_loss_decreases_with_more_training(training_data):
    """The optimiser must actually be learning, not just running."""
    X, y = training_data
    losses = ModelTrainer().loss_curve(X, y, steps=(1, 5, 20, 100))
    assert losses[-1] < losses[0]
    # Monotonic (allowing a tiny numerical wobble).
    assert all(b <= a + 1e-6 for a, b in zip(losses, losses[1:]))


def test_model_can_overfit_a_small_batch(training_data):
    """If it cannot memorise 20 rows, the pipeline is broken."""
    X, y = training_data
    # 10 of each class, so the batch is learnable and not trivially imbalanced.
    index = list(y[y == 0].index[:10]) + list(y[y == 1].index[:10])
    batch_X, batch_y = X.loc[index], y.loc[index]

    # Regularisation turned off -> the model is free to memorise.
    trainer = ModelTrainer(max_iter=5000)
    pipeline = trainer._new_pipeline()
    pipeline.named_steps["model"].set_params(C=1e6)
    pipeline.fit(batch_X, batch_y)

    assert pipeline.score(batch_X, batch_y) > 0.95


def test_trained_model_beats_the_release_gate(training_data):
    X, y = training_data
    trainer = ModelTrainer()
    pipeline = trainer.fit(X, y)
    y_prob = pipeline.predict_proba(X)[:, 1]

    scores = evaluate_model(y, y_prob)
    assert scores["accuracy"] >= MIN_ACCURACY
    assert scores["f1"] >= MIN_F1
    assert scores["roc_auc"] > 0.5  # better than a coin flip


def test_model_beats_a_majority_class_baseline(training_data):
    """Accuracy alone can lie on imbalanced data - compare to the dumb model."""
    X, y = training_data
    pipeline = ModelTrainer().fit(X, y)
    baseline = max(y.mean(), 1 - y.mean())
    assert pipeline.score(X, y) > baseline


def test_training_is_reproducible(training_data):
    X, y = training_data
    a = ModelTrainer(seed=42).fit(X, y).predict_proba(X)[:, 1]
    b = ModelTrainer(seed=42).fit(X, y).predict_proba(X)[:, 1]
    assert np.allclose(a, b)


def test_save_before_fit_raises():
    with pytest.raises(RuntimeError, match="fit"):
        ModelTrainer().save()
