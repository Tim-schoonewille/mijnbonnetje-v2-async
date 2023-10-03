import { Button, Flex, useDisclosure, Link } from "@chakra-ui/react";
import React, { useRef } from "react";
import { ColorModeSwitcher } from "../../ColorModeSwitcher";
import { HamburgerIcon } from "@chakra-ui/icons";
import { Link as NavLink } from "react-router-dom";

import {
  Drawer,
  DrawerBody,
  DrawerFooter,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
} from "@chakra-ui/react";
import { navLinkMapping } from "./NavBar";
import { useAuthContext } from "../../context/AuthContext";

type NavMobileProps = {
  links: navLinkMapping[];
};
export default function NavMobile({ links }: NavMobileProps) {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const { isLoggedIn } = useAuthContext();
  return (
    <Flex
      display={["flex", "flex", "none", "none"]}
      alignItems="center"
      justifyContent="space-between"
      gap={10}
      pr={5}
    >
      <ColorModeSwitcher justifySelf="flex-end" />
      <Button colorScheme="teal" onClick={onOpen}>
        <HamburgerIcon />
      </Button>

      <Drawer isOpen={isOpen} placement="top" onClose={onClose}>
        <DrawerOverlay />
        <DrawerContent>
          <DrawerCloseButton />
          <DrawerHeader m="0 auto" pr={19}></DrawerHeader>

          <DrawerBody>
            <Flex
              as="ul"
              flexDirection={"column"}
              listStyleType="none"
              justifyContent="flex-end"
            >
              {links.map((navlink) => {
                return (
                  <Link as="li" key={navlink.route} ml="auto" fontSize="4xl">
                    <NavLink to={navlink.route} onClick={onClose}>
                      {navlink.name}
                    </NavLink>
                  </Link>
                );
              })}
            </Flex>
          </DrawerBody>

          <DrawerFooter>
            <Flex gap={5}>
              {isLoggedIn ? (
                <NavLink to="/auth/logout">
                  <Button colorScheme="teal" w="auto" onClick={onClose}>
                    Logout
                  </Button>
                </NavLink>
              ) : (
                <>
                  <NavLink to="/auth/login">
                    <Button colorScheme="teal" w="auto" onClick={onClose}>
                      Login
                    </Button>
                  </NavLink>
                  <NavLink to="/auth/register">
                    <Button
                      colorScheme="teal"
                      variant="outline"
                      w="auto"
                      onClick={onClose}
                    >
                      register
                    </Button>
                  </NavLink>
                </>
              )}
            </Flex>
          </DrawerFooter>
        </DrawerContent>
      </Drawer>
    </Flex>
  );
}
