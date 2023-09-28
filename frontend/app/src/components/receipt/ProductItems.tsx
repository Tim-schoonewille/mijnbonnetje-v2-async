import React from "react";
import SingleProductItem from "./SingleProductItem";
import { Flex, Icon, Text } from "@chakra-ui/react";

import { MdProductionQuantityLimits} from 'react-icons/md'
import { ProductItem } from "../../client";

type ProductItemsProps = {
  productItems: ProductItem[] | undefined | null
}
export default function ProductItems({productItems}: ProductItemsProps) {
  if (productItems === null || productItems === undefined) return <Text>Error loading products</Text>
  return (
    <>
      <Flex flexDirection="column" gap={3}>
        <Text as="b">
          <Icon as={MdProductionQuantityLimits} mr="9px" /> Product Items
        </Text>
        <Flex flexDirection="column" gap='12px'>
          {productItems.map((product) => {
            return <SingleProductItem key={product.id} product={product}/>;
          })}
        </Flex>
      </Flex>
    </>
  );
}
