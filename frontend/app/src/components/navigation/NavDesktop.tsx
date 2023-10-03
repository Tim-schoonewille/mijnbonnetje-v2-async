import React from "react";
import { navLinkMapping } from "./NavBar";
import { Button, Flex, Link } from "@chakra-ui/react";
import { Link as NavLink } from "react-router-dom";
import { ColorModeSwitcher } from "../../ColorModeSwitcher";
import { useAuthContext } from "../../context/AuthContext";

type NavDesktopProps = {
  links: navLinkMapping[];
};
export default function NavDesktop({ links }: NavDesktopProps) {
  const { isLoggedIn } = useAuthContext();
  return (
    <Flex display={["none", "none", "flex", "flex"]} gap="60px">
      <Flex
        as="ul"
        justifyContent="space-between"
        alignItems="center"
        listStyleType="none"
        gap={6}
        p={1}
      >
        {links.map((navlink) => {
          return (
            <Link as="li" key={navlink.route}>
              <NavLink to={navlink.route}>{navlink.name}</NavLink>
            </Link>
          );
        })}
      </Flex>
      <ColorModeSwitcher justifySelf="flex-end" />
      <Flex as="ul" justifyContent="space-between" alignItems="center" gap={2}>
        {isLoggedIn ? (
          <>
            <NavLink to="/auth/logout">
              <Button colorScheme="teal">Logout</Button>
            </NavLink>
          </>
        ) : (
          <>
            <NavLink to="/auth/login">
              <Button variant="outline" colorScheme="teal">
                Login
              </Button>
            </NavLink>
            <NavLink to="/auth/register">
              <Button colorScheme="teal">Register</Button>
            </NavLink>
          </>
        )}
      </Flex>
    </Flex>
  );
}
