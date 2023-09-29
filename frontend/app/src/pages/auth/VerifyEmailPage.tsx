import { Flex, Link, Text, useToast } from "@chakra-ui/react";
import React, { useEffect, useState } from "react";
import { useSearchParams, Link as NavLink } from "react-router-dom";
import { AuthService } from "../../client";

export default function VerifyEmailPage() {
  const [queryParams] = useSearchParams();
  const emailVerificationToken = queryParams.get("token") ?? "invalidtoken";
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false)
  const toast = useToast()

  async function handleEmailVerification(token: string) {
    try {
      setIsLoading(true)
      const response = await AuthService.authVerifyEmail(token)

      if (response.status === 200) {
        setSuccessMessage('E-mail succesfully verified, you can now proceed to login!')
        toast({
          title: 'Email verified',
          description: 'You can now proceed to login',
          status: 'success',
          duration: 5000,
          isClosable: true
        })

      } else {
        setErrorMessage('Something went wrong, request a new token')
      }

    } catch (e) {
      console.error(e)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    if (!emailVerificationToken) return

    handleEmailVerification(emailVerificationToken)
  }, [emailVerificationToken])
  return (
    <Flex
      justifyContent="center"
      alignItems="center"
      flexDirection="column"
      gap={15}
    >

      {successMessage && <Text color={'green.400'}> {successMessage} </Text> }
      {errorMessage && <>
      
      <Text color={'red.400'}> {errorMessage }</Text>
      <Link as='div'><NavLink to='/auth/request-new-email-verification'>Request new token</NavLink></Link>
      </>
      }
    
    </Flex>
  );
}
