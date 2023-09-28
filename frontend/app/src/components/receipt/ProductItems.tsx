import React from "react";
import SingleProductItem from "./SingleProductItem";
import { Flex, Icon, Text } from "@chakra-ui/react";

import { MdProductionQuantityLimits} from 'react-icons/md'

export default function ProductItems() {
  const foo = [1, 1, 1, 1, 1, 1, 1, 1, 1,1,1,1,1,1,1,1,1,1,1,1];
  return (
    <>
      <Flex flexDirection="column" gap={3}>
        <Text as="b">
          <Icon as={MdProductionQuantityLimits} mr="9px" /> Product Items
        </Text>
        <Flex flexDirection="column" gap='12px'>
          {foo.map((product) => {
            return <SingleProductItem />;
          })}
        </Flex>
      </Flex>
    </>
  );
}
