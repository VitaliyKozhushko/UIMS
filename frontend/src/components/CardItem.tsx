import { Card, Image, Text, Badge, Button, Group, Avatar } from '@mantine/core';
import card from '../assets/scss/card.module.scss';

interface CardProps {
  mainCss: string
}

function CardItem(props: CardProps) {
  const { mainCss } = props;

  return (
    <Card className={card[mainCss]} shadow="sm" padding="lg" radius="md" withBorder>
      <Card.Section className={card.avatarBlock}>
        <Avatar className={card.avatar} variant="light" radius="md" size="xl" src="" />
      </Card.Section>

      <Group justify="space-between" mt="md" mb="xs">
        <Text fw={500}>Norway Fjord Adventures</Text>
        <Badge color="pink">On Sale</Badge>
      </Group>

      <Text size="sm" c="dimmed">
        With Fjord Tours you can explore more of the magical fjord landscapes with tours and
        activities on and around the fjords of Norway
      </Text>

      <Button color="blue" fullWidth mt="md" radius="md">
        Book classic tour now
      </Button>
    </Card>
  );
}

export default CardItem