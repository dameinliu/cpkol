# 构建阶段
FROM node:20-alpine AS build

WORKDIR /app

# 复制package文件
COPY package.json pnpm-lock.yaml ./

# 安装pnpm和依赖
RUN npm install -g pnpm && \
    pnpm install --frozen-lockfile

# 复制源码并构建
COPY . .
RUN pnpm run build

# 生产阶段
FROM nginx:alpine AS production

# 安装curl用于健康检查
RUN apk add --no-cache curl

# 复制构建产物
COPY --from=build /app/dist /usr/share/nginx/html

# 复制Nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 移除默认配置
RUN rm /etc/nginx/conf.d/default.conf.bak 2>/dev/null || true

# 设置正确的权限
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# 暴露端口
EXPOSE 80

# 切换到非root用户
USER nginx

# 启动Nginx
CMD ["nginx", "-g", "daemon off;"]
