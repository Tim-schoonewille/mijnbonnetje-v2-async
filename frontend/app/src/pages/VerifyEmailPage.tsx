import React, { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { AuthService } from "../client";
import { Center, Text } from "@chakra-ui/react";

export default function VerifyEmailPage() {
  const [validEmailToken, setValidEmailToken] = useState(false);
  const [queryParams] = useSearchParams();
  const navigate = useNavigate();

  const emailVerificationToken = queryParams.get("token") ?? "invalidtoken";

  const verifyEmailToken = async () => {
    const response = await AuthService.authVerifyEmail(emailVerificationToken);
    if (response.status === 200) {
      setValidEmailToken(true);
    } else {
      setValidEmailToken(false);
    }
  };
  useEffect(() => {
    verifyEmailToken();
  }, []);
  return (
    <>
      <Center>
        <Text mt={10} color={
            validEmailToken ? 'green.500' : 'red.500'
        }>
          {validEmailToken
            ? "Your email is now verified, you can proceed to login"
            : "Invalid token, please request a new one!"}
        </Text>
      </Center>
    </>
  );
}
