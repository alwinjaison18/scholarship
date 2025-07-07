import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export function useRoleRedirect() {
  const { data: session, status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (status === "loading") return;

    if (!session) {
      router.push("/auth/signin");
      return;
    }

    // Redirect based on user role
    const pathname = window.location.pathname;

    if (session.user.role === "admin") {
      // Admin users trying to access regular dashboard should go to admin panel
      if (pathname === "/dashboard") {
        router.push("/admin");
        return;
      }
    } else {
      // Regular users trying to access admin routes should go to dashboard
      if (
        pathname.startsWith("/admin") ||
        pathname.startsWith("/test-scraping")
      ) {
        router.push("/dashboard");
        return;
      }
    }
  }, [session, status, router]);

  return { session, status };
}

export function useRequireAuth(requiredRole?: string) {
  const { data: session, status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (status === "loading") return;

    if (!session) {
      router.push("/auth/signin");
      return;
    }

    if (requiredRole && session.user.role !== requiredRole) {
      if (session.user.role === "admin") {
        router.push("/admin");
      } else {
        router.push("/dashboard");
      }
      return;
    }
  }, [session, status, router, requiredRole]);

  return {
    session,
    status,
    isAuthorized:
      !!session && (!requiredRole || session.user.role === requiredRole),
  };
}

export function useRequireAdmin() {
  return useRequireAuth("admin");
}
