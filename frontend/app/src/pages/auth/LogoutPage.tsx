import { Text } from "@chakra-ui/react";
import React, { useEffect } from "react";
import { useAuthContext } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { AuthService } from "../../client";

export default function LogoutPage() {
  const { isLoggedIn, setIsLoggedIn } = useAuthContext();
  const navigate = useNavigate();

  useEffect(() => {
    async function handleLogout() {
      try {
        const response = await AuthService.authLogout();
        if (response.status === 200) {
          setIsLoggedIn(false);
          navigate("/auth/login");
        }
      } catch (e) {
        console.error(e);
      }
    }
    handleLogout();
  }, [navigate, setIsLoggedIn]);
  return <Text>Logging out...</Text>;
}
