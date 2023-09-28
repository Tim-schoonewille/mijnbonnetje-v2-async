import React from "react";
import { navLinkMapping } from "./NavBar";
import { Button, Flex, Link } from "@chakra-ui/react";
import { Link as NavLink } from "react-router-dom";
import { ColorModeSwitcher } from "../../ColorModeSwitcher";

type NavDesktopProps = {
  links: navLinkMapping[];
};
export default function NavDesktop({ links }: NavDesktopProps) {
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
        <NavLink to="/auth/login">
          <Button>Login</Button>
        </NavLink>
        <NavLink to="/auth/register">
          <Button variant='outline'>Register</Button>
        </NavLink>
      </Flex>
    </Flex>
  );
}
