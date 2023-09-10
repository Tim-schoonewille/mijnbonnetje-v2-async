import React, { FormEvent } from "react";
import { AuthService } from "../client";

export default function Logout({
  onLogout,
}: {
  onLogout: (value: any) => void;
}) {
  async function handleLogout(e: FormEvent) {
    e.preventDefault();
    try {
      await AuthService.authLogout()
      onLogout(false)
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
