import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: {
    provider: "sqlite",
    url: ":memory:", // In-memory for frontend-only session management
  },
  emailAndPassword: {
    enabled: true,
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // Update session every 24 hours
  },
  secret: process.env.BETTER_AUTH_SECRET || "",
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
});

export type Session = typeof auth.$Infer.Session;
