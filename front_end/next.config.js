/**
 * Run `build` or `dev` with `SKIP_ENV_VALIDATION` to skip env validation. This is especially useful
 * for Docker builds.
 */
await import("./src/env.js");

/** @type {import('next').NextConfig} */
const nextConfig = {
    rewrites: async () => {
      return [
        {
          source: '/:path*',
          destination: 'http://127.0.0.1:4000/:path*'
        },
      ]
    },
  }
  
export default nextConfig;
