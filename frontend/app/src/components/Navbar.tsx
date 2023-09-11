import React from "react";
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

const Navbar: React.FC = () => {
  const { isLoggedIn, setIsLoggedIn } = useAuthContext();
  return (
    <Box as="nav" bg="blue.500" p={4} color="white">
      <Flex align="center">
        <Link to="/">
          <Text fontSize="xl" fontWeight="bold">
            mijnbonnetje.lan
          </Text>
        </Link>
        <Spacer />
        <Link to="/add-receipt">
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
        {isLoggedIn ? (
          <Link to="/logout">
            <ChakraLink as="span">
              <Button colorScheme="teal" size="sm">
                Logout
              </Button>
            </ChakraLink>
          </Link>
        ) : (
          <>
            <Link to="/login">
              <ChakraLink as="span">
                <Button colorScheme="teal" size="sm">
                  Login
                </Button>
              </ChakraLink>
            </Link>

            <Link to="/register">
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
