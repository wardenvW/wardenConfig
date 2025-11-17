PREFIX ?= /usr/local
VENV_DIR = venv
BIN_DIR = $(PREFIX)/bin

help:
	@echo "-----------------------------------------"
	@echo " "
	@echo " make install - to install Wardenconfig"
	@echo " "
	@echo "----------------------------------------"

install:
	@echo "🚀 Installing wconfig..."

	python3 -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/python -m pip install --upgrade pip
	$(VENV_DIR)/bin/python -m pip install .

	@echo "📦 Copying wconfig to $(BIN_DIR)..."

	mkdir -p $(BIN_DIR)
	cp $(VENV_DIR)/bin/wconfig $(BIN_DIR)/

	@echo "✅ Success!"
	@echo "Run 'wconfig' to show interfaces"

clean:
	@echo "🧹 Cleaning..."
	rm -rf $(VENV_DIR)
	@echo "Done."

uninstall:
	sudo rm -f $(BIN_DIR)/wconfig


.PHONY: help install clean uninstall
