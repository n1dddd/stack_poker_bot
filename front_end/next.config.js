/**
 * Run `build` or `dev` with `SKIP_ENV_VALIDATION` to skip env validation. This is especially useful
 * for Docker builds.
 */
await import("./src/env.js");

/** @type {import('next').NextConfig} */
const nextConfig = {
    images: {
      domains: ["encrypted-tbn0.gstatic.com", 'cdn.discordapp.com']
    }
  }
  
export default nextConfig;
