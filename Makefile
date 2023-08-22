# Define default input and output directories
INPUT=data
OUTPUT=output

# Define the app script
APP_SCRIPT=app.py

# Run the app
run:
	python $(APP_SCRIPT) $(INPUT) $(OUTPUT)

# Define the commit message
MSG ?= "Update project"

# Commit and push changes to the Git repository
# make push MSG="My custom commit message"
push:
	git add .
	git commit -m $(MSG)
	git push origin master

# Clean output files
clean:
	rm -rf $(OUTPUT)/*

# Visualize data with Streamlit
visualize:
	streamlit run streamlit_app.py

# Install required packages
install:
	pip install -r requirements.txt

# Run the app and visualize data with Streamlit
all: run visualize
