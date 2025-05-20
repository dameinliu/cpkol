.PHONY: help backend frontend install-backend install-frontend run-backend run-frontend

help:
	@echo "用法："
	@echo "  make install-backend   # 安装后端依赖"
	@echo "  make install-frontend  # 安装前端依赖"
	@echo "  make run-backend       # 启动后端服务"
	@echo "  make run-frontend      # 启动前端服务"
	@echo "  make backend           # 安装并启动后端"
	@echo "  make frontend          # 安装并启动前端"

install-backend:
	cd backend && pip install -r ../requirements.txt

install-frontend:
	cd frontend && yarn install

run-backend:
	cd backend && python app.py

run-frontend:
	cd frontend && yarn dev

backend: install-backend run-backend

frontend: install-frontend run-frontend
