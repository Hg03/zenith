full:
    @echo "Running Full Pipeline (Feature + Training)"
    @python src/zenith/app/training_endpoint.py

feature:
    @echo "Running Feature Pipeline"
    @python src/zenith/app/training_endpoint.py steps.pipeline=feature

train:
    @echo "Running Training Pipeline"
    @python src/zenith/app/training_endpoint.py steps.pipeline=training