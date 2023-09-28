import React, { FC, ReactNode, useContext, useEffect } from "react";
import { AuthService } from "../client";
import { useAuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { useToast } from "@chakra-ui/react";

export default function RequiresValidToken({ children }: { children: any }) {
  const { setIsLoggedIn, setTokenIsVerified, tokenIsVerified } =
    useAuthContext();
  const navigate = useNavigate();
  const toast = useToast();
  useEffect(() => {
    async function checkTokenValidity() {
      try {
        const response = await AuthService.authVerifyToken();

        if (response.status === 200) {
          setTokenIsVerified(true);
          setIsLoggedIn(true);
        }
        else if (response.body['detail'] === 'EMAIL_NOT_VERIFIED') {
          toast({
            title: "Verify your email!",
            description: "Please check your inbox to for an email verification link",
            status: 'info',
            duration: 10000,
            isClosable: true,
          })
          setIsLoggedIn(true)
          navigate('/auth/verify-email/new')
        }
        else if (response.status !== 200) {
            toast({
                title:'Requires login',
                description:'The page you tried to visit requires a login!',
                status:'warning',
                duration: 4000,
                isClosable: true,
            })
          setTokenIsVerified(false);
          navigate("/auth/login");
        }
      } catch (e) {
        console.error(e);
      }
    }
    checkTokenValidity();
  }, [setTokenIsVerified, setIsLoggedIn, navigate, toast]);

  if (!tokenIsVerified) {
    return <h1>Requires token!</h1>;
  }
  return <>{children};</>;
}