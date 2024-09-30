import {
  Paper,
  PaperProps,
  Button,
  Divider,
} from '@mantine/core';
import authImg from '../assets/img/images/auth_card.png'
import { useNavigate } from "react-router-dom";

interface CustomProps {
  css: string;
  cssimg: string;
}

type AuthFormProps = PaperProps & CustomProps;

function AuthForm(props: AuthFormProps) {
  const { css, cssimg } = props;

  const navigate = useNavigate();

  function authUser() {
    const currentTime = new Date().getTime();
    localStorage.setItem('loginTime', currentTime.toString());
    console.log('authUser')
    navigate('/lk')
  }

  return (
    <Paper className={css} radius="md" p="xl" withBorder {...props}>
      <img className={cssimg} src={authImg} alt='auth'></img>
      <Divider labelPosition="center" my="lg" />

      <Button variant="filled" onClick={authUser}>Вход</Button>
    </Paper>
  );
}

export default AuthForm;