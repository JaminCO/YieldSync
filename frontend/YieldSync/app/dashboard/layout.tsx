'use client'
import NavBar from "./NavBar";
import SideBar from "./SideBar";
import { SideBarProvider } from "./SideBarContext";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  
  return (
    <SideBarProvider>
      {/* ✅ FIX: Add background color */}
      <div className="min-h-screen lg:flex">
        <SideBar />
        
        {/* ✅ FIX: Use flex-1 min-w-0 instead of w-full */}
        <main className="flex-1 min-w-0">
          <NavBar />
          {children}
        </main>
      </div>
    </SideBarProvider>
  );
}