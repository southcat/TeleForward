# 使用Node.js镜像作为基础镜像来构建前端
FROM node:21.5.0 AS frontend-builder

# 设置工作目录
WORKDIR /app/web

# 复制前端项目文件
COPY web/package*.json ./
RUN npm install

COPY web .

# 构建前端项目
RUN npm run build

# 使用Python镜像作为基础镜像
FROM python:3.12.1

# 安装Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_21.x | bash - && \
    apt-get install -y nodejs

# 设置工作目录
WORKDIR /app

# 复制整个项目到容器中，包括虚拟环境
COPY . /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*
RUN  pip install --no-cache-dir -r requirements.txt
ENV PATH=/app/.venv/bin:$PATH

# 激活虚拟环境并安装额外的Python依赖（如果需要）
# RUN . .venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# 从前端构建阶段复制构建后的文件
COPY --from=frontend-builder /app/web/.next /app/web/.next
COPY --from=frontend-builder /app/web/public /app/web/public
COPY --from=frontend-builder /app/web/package*.json /app/web/

# 安装Next.js运行时依赖
WORKDIR /app/web
RUN npm install --production

# 返回主工作目录
WORKDIR /app


# 暴露应用端口
EXPOSE 8000 3000

# 创建启动脚本
RUN echo '#!/bin/bash\n\
cd /app/web && npm start &\n\
cd /app && python -m uvicorn main:app --host 0.0.0.0 --port 8000\n\
' > /app/start.sh && chmod +x /app/start.sh

# 启动命令
CMD ["/bin/bash", "/app/start.sh"]