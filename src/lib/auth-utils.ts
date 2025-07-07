// Mock users for development (when database is not available)
const mockUsers = [
  {
    id: "1",
    email: "admin@shikshasetu.com",
    password: "admin123",
    name: "Admin User",
    role: "admin",
  },
  {
    id: "2",
    email: "test@shikshasetu.com",
    password: "test123",
    name: "Test User",
    role: "student",
  },
];

export async function authenticateUser(email: string, password: string) {
  // First try to find user in mock data
  const mockUser = mockUsers.find(
    (user) => user.email === email && user.password === password
  );

  if (mockUser) {
    return {
      id: mockUser.id,
      email: mockUser.email,
      name: mockUser.name,
      role: mockUser.role,
    };
  }

  // If not found in mock data, try database (if available)
  try {
    const { prisma } = await import("@/lib/prisma");
    const { compare } = await import("bcryptjs");

    const user = await prisma.user.findUnique({
      where: { email },
    });

    if (!user || !user.passwordHash) {
      return null;
    }

    const isPasswordValid = await compare(password, user.passwordHash);

    if (!isPasswordValid) {
      return null;
    }

    return {
      id: user.id,
      email: user.email,
      name: user.fullName || user.email,
      role: user.role,
    };
  } catch (error) {
    console.log("Database not available, using mock authentication", error);
    return null;
  }
}
