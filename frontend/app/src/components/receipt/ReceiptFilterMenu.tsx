import { CalendarIcon } from "@chakra-ui/icons";
import {
  AccordionButton,
  AccordionIcon,
  AccordionItem,
  AccordionPanel,
  Box,
  Flex,
  Icon,
  Input,
  Select,
} from "@chakra-ui/react";
import React from "react";
import { BsShop } from "react-icons/bs";
import { BiCategoryAlt } from "react-icons/bi";
import { HiOutlineFilter } from "react-icons/hi";
import { Categories, Store } from "../../client";

type ReceiptFilterMenuProps = {
  stores: Store[] | null;
};
export default function ReceiptFilterMenu({ stores }: ReceiptFilterMenuProps) {
  const accordionMargin = [0, 0, "200px", "500px"];
  const categories = Object.values(Categories);
  return (
    <AccordionItem ml={accordionMargin} mr={accordionMargin}>
      <h2>
        <AccordionButton>
          <Box as="span" flex="1" textAlign="left">
            <Icon as={HiOutlineFilter} />
            &nbsp; Filters
          </Box>
          <AccordionIcon />
        </AccordionButton>
      </h2>
      <AccordionPanel pb={4}>
        <Flex direction={"column"} as="ul" listStyleType={"none"} gap={3}>
          <Flex as="li" gap="4px" justifyContent="center" alignItems="center">
            <Icon as={CalendarIcon} mr="12px" />
            <Input type="date" />
            <Input type="date" />
          </Flex>
          <Flex as="li" gap="4px" justifyContent="center" alignItems="center">
            <Icon as={BsShop} mr="12px" />
            <Select placeholder="select shop">
              {stores?.map((store) => {
                return <option key={store.id}>{store.name}</option>;
              })}
            </Select>
          </Flex>

          <Flex as="li" gap="4px" justifyContent="center" alignItems="center">
            <Icon as={BiCategoryAlt} mr="12px" />
            <Select placeholder="select category">
              {categories.map((category, i) => {
                return <option key={i}>{category}</option>;
              })}
            </Select>
          </Flex>
        </Flex>
      </AccordionPanel>
    </AccordionItem>
  );
}
