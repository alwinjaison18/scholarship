#!/usr/bin/env node

// Database connection test script
const { PrismaClient } = require("@prisma/client");

async function testDatabaseConnection() {
  const prisma = new PrismaClient();

  try {
    console.log("🔍 Testing database connection...");

    // Test connection
    await prisma.$connect();
    console.log("✅ Database connection successful!");

    // Check if users table exists and has data
    const userCount = await prisma.user.count();
    console.log(`📊 Users in database: ${userCount}`);

    if (userCount === 0) {
      console.log("⚠️  No users found in database.");
      console.log(
        "💡 Run: npm run seed-users (if available) or create users manually"
      );
    } else {
      // List existing users
      const users = await prisma.user.findMany({
        select: {
          email: true,
          role: true,
          isActive: true,
        },
      });

      console.log("👥 Existing users:");
      users.forEach((user) => {
        console.log(
          `   - ${user.email} (${user.role}) ${user.isActive ? "✅" : "❌"}`
        );
      });
    }
  } catch (error) {
    console.log("❌ Database connection failed:");
    console.log("   Error:", error.message);
    console.log("");
    console.log("🔧 Troubleshooting:");
    console.log("   1. Check if PostgreSQL is running");
    console.log("   2. Verify DATABASE_URL in .env.local");
    console.log("   3. Run: npx prisma db push (to create tables)");
    console.log("   4. Run: npx prisma generate (to generate client)");
    console.log("");
    console.log("📝 Current DATABASE_URL format should be:");
    console.log(
      "   postgresql://username:password@localhost:5432/database_name"
    );
  } finally {
    await prisma.$disconnect();
  }
}

async function createMockUsers() {
  const prisma = new PrismaClient();

  try {
    console.log("👤 Creating mock users...");

    // Create admin user
    await prisma.user.upsert({
      where: { email: "admin@shikshasetu.com" },
      update: {},
      create: {
        username: "admin",
        email: "admin@shikshasetu.com",
        passwordHash:
          "$2a$10$rQ5gxFKdBYuaQJmyBkbCge2ZjTZfJ/jGjQdYKhAhpqJrLHVR6yXfm", // admin123
        fullName: "Admin User",
        role: "admin",
        isActive: true,
        emailVerified: true,
      },
    });

    // Create test user
    await prisma.user.upsert({
      where: { email: "test@shikshasetu.com" },
      update: {},
      create: {
        username: "testuser",
        email: "test@shikshasetu.com",
        passwordHash:
          "$2a$10$rQ5gxFKdBYuaQJmyBkbCge2ZjTZfJ/jGjQdYKhAhpqJrLHVR6yXfm", // test123
        fullName: "Test User",
        role: "student",
        isActive: true,
        emailVerified: true,
      },
    });

    console.log("✅ Mock users created successfully!");
  } catch (error) {
    console.log("❌ Failed to create users:", error.message);
  } finally {
    await prisma.$disconnect();
  }
}

// Main execution
async function main() {
  console.log("🚀 ShikshaSetu Database Setup Check\n");

  await testDatabaseConnection();

  console.log("\n🔄 Would you like to create mock users? (y/n)");

  // In a real scenario, you'd want to prompt for user input
  // For now, we'll just show the command
  console.log("💡 To create mock users, run: node scripts/create-users.js");
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { testDatabaseConnection, createMockUsers };
