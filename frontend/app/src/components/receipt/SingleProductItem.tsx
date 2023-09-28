import { Flex, Text } from "@chakra-ui/react";
import React from "react";
import { ProductItem } from "../../client";

type SingleProductItemProps = {
  product: ProductItem
}

export default function SingleProductItem({ product }: SingleProductItemProps) {
  return (
    <Flex alignItems="center" justifyContent="space-between">
      <Text as="i">{product.quantity} x</Text>
      <Text as="i">{product.name }</Text>
      <Text as="i"> € {product.price} </Text>
    </Flex>
  );
}
