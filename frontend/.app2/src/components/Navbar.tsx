import React, { useEffect } from "react";
import { Link } from "react-router-dom";
import {
  Box,
  Flex,
  Spacer,
  Text,
  Link as ChakraLink,
  Button,
} from "@chakra-ui/react";
import { useAuthContext } from "../context/AuthContext";
import { AuthService } from "../client";

const Navbar: React.FC = () => {
  const { isLoggedIn, setIsLoggedIn } = useAuthContext();

  useEffect(() => {
    async function verifyToken() {
      try {
        const response = await AuthService.authVerifyToken();
        if (response.status === 200) {
          setIsLoggedIn(true);
        }
      } catch (e) {
        console.error(e);
      }
    }
    verifyToken();
  }, [setIsLoggedIn]);
  return (
    <Box as="nav" bg="blue.500" p={4} color="white">
      <Flex align="center" m="0 auto" maxWidth="1200px">
        <Link to="/">
          <Text fontSize="xl" fontWeight="bold">
            mijnbonnetje.lan
          </Text>
        </Link>
        <Spacer />
        {isLoggedIn && (
          <>
            <Link to="/addreceipt">
              <ChakraLink as="span" mr={4}>
                Add Receipt
              </ChakraLink>
            </Link>
            <Link to="/receipts">
              <ChakraLink as="span" mr={4}>
                Receipts
              </ChakraLink>
            </Link>
            <Link to="/categories">
              <ChakraLink as="span" mr={4}>
                Categories
              </ChakraLink>
            </Link>
            <Link to="/stores">
              <ChakraLink as="span" mr={4}>
                Stores
              </ChakraLink>
            </Link>
          </>
        )}
        <Spacer />
        {isLoggedIn ? (
          <Link to="/auth/logout">
            <ChakraLink as="span">
              <Button colorScheme="teal" size="sm">
                Logout
              </Button>
            </ChakraLink>
          </Link>
        ) : (
          <>
            <Link to="/auth/login">
              <ChakraLink as="span">
                <Button colorScheme="teal" size="sm">
                  Login
                </Button>
              </ChakraLink>
            </Link>

            <Link to="/auth/register">
              <ChakraLink as="span">
                <Button colorScheme="teal" size="sm" ml={2}>
                  Register
                </Button>
              </ChakraLink>
            </Link>
          </>
        )}
      </Flex>
    </Box>
  );
};

export default Navbar;
