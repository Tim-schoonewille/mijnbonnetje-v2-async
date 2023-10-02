import { CalendarIcon } from "@chakra-ui/icons";
import {
  AccordionButton,
  AccordionIcon,
  AccordionItem,
  AccordionPanel,
  Box,
  Button,
  Flex,
  Icon,
  Input,
  Select,
} from "@chakra-ui/react";
import React, { useState } from "react";
import { BsShop } from "react-icons/bs";
import { BiCategoryAlt } from "react-icons/bi";
import { HiOutlineFilter } from "react-icons/hi";
import { Categories, Store } from "../../client";
import { useLocation, useNavigate } from "react-router-dom";

type ReceiptFilterMenuProps = {
  stores: Store[] | null;
};
export default function ReceiptFilterMenu({ stores }: ReceiptFilterMenuProps) {
  const accordionMargin = [0, 0, "200px", "500px"];
  const categories = Object.values(Categories);
  const [filtersAreSet, setFiltersAreSet] = useState(false);

  const location = useLocation();
  const navigate = useNavigate();
  const queryParams = new URLSearchParams(location.search);
  const updateQueryParamsAndNavigate = (category: string) => {
    setFiltersAreSet(true);
    queryParams.set("category", category);
    const newSearch = queryParams.toString();

    navigate(`/receipts?${newSearch}`);
  };
  const updateShopParams = (shop: string) => {
    setFiltersAreSet(true);
    queryParams.set("shop", shop);
    const newSearch = queryParams.toString();
    navigate(`/receipts?${newSearch}`);
  };
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
            <Select
              placeholder="select shop"
              onChange={(e) => updateShopParams(e.target.value)}
            >
              {stores?.map((store) => {
                return <option key={store.id}>{store.name}</option>;
              })}
            </Select>
          </Flex>

          <Flex as="li" gap="4px" justifyContent="center" alignItems="center">
            <Icon as={BiCategoryAlt} mr="12px" />
            <Select
              placeholder="select category"
              onChange={(e) => updateQueryParamsAndNavigate(e.target.value)}
            >
              {categories.map((category, i) => {
                return <option key={i}>{category}</option>;
              })}
            </Select>
          </Flex>
          {filtersAreSet && (
            <Button
              onClick={() => {
                setFiltersAreSet(false);
                navigate('/receipts')
              }}
            >
              Remove filters
            </Button>
          )}
        </Flex>
      </AccordionPanel>
    </AccordionItem>
  );
}
