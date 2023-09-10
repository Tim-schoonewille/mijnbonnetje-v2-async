import React, { FormEvent } from "react";

export default function Logout({
  onLogout,
}: {
  onLogout: (value: any) => void;
}) {
  async function handleLogout(e: FormEvent) {
    e.preventDefault();
    try {
      const response = await fetch(
        "http://backend.mijnbonnetje.lan:8000/auth/logout",
        {
          method: "GET",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
        }
      );
      if (response.ok) {
        onLogout(false);
      } else {
        console.log("logout failed");
      }
    } catch (error) {
      console.error("error:", error);
    }
  }
  return (
    <div>
      <form>
        <button onClick={handleLogout}>Logout</button>
      </form>
    </div>
  );
}
