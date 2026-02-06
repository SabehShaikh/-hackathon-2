# Phase 4: Todo AI Chatbot Frontend
# Multi-stage production build for Kubernetes deployment
# AI Tool: Gordon - docker ai "create multi-stage production dockerfile for next.js 16 standalone"

# =============================================================================
# Stage 1: Dependencies - Install node modules
# =============================================================================
FROM node:20-alpine AS deps

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install ALL dependencies (including dev for build)
RUN npm ci

# =============================================================================
# Stage 2: Builder - Build the application
# =============================================================================
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules

# Copy source code
COPY . .

# Build-time environment variables
ARG NEXT_PUBLIC_API_URL=http://localhost:30800
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Build the application
RUN npm run build

# =============================================================================
# Stage 3: Runner - Production runtime
# =============================================================================
FROM node:20-alpine AS runner

WORKDIR /app

# Set production environment
ENV NODE_ENV=production

# Create non-root user for security (FR-005)
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001 -G nodejs

# Copy public assets
COPY --from=builder /app/public ./public

# Copy standalone build output
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Switch to non-root user
USER nextjs

# Expose port 3000 (Kubernetes service port)
EXPOSE 3000

# Set port environment variable
ENV PORT=3000 \
    HOSTNAME="0.0.0.0"

# Health check for Kubernetes probes (FR-006)
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

# Run the standalone server
CMD ["node", "server.js"]
