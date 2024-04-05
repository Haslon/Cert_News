const mysql = require('mysql');
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();

// Configuración de conexión a la base de datos
const pool = mysql.createPool({
  connectionLimit: 10,
  host: '127.0.0.1',
  user: 'root',
  database: 'cert',
});

// Iniciar el servidor en el puerto 3000
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Servidor en ejecución en http://localhost:${PORT}`);
});

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Configuración CORS
app.use(cors());

// Ruta para manejar la solicitud POST desde el formulario HTML para guardar registros
app.post('/guardar_registro', (req, res) => {
  const { correo, contraseña } = req.body;

  // Insertar los datos en la base de datos
  pool.query('INSERT INTO usuarios (correo, contraseña) VALUES (?, ?)', [correo, contraseña], (error, results) => {
    if (error) {
      console.error('Error al insertar datos:', error);
      return res.status(500).json({ message: 'Error al guardar los datos' });
    }
    console.log('Datos insertados correctamente');
    res.status(200).json({ message: 'Datos insertados correctamente' });
  });
});

app.post('/login', (req, res) => {
    const { correo, contraseña } = req.body;
  
    // Verificar si el correo y la contraseña coinciden con los registros en la base de datos
    pool.query('SELECT * FROM usuarios WHERE correo = ? AND contraseña = ?', [correo, contraseña], (error, results) => {
      if (error) {
        console.error('Error al buscar usuario:', error);
        return res.status(500).json({ message: 'Error al buscar usuario' });
      }
  
      // Si hay resultados, el usuario existe y la contraseña es correcta
      if (results.length > 0) {
        // Si la autenticación es exitosa, envía una respuesta exitosa
        res.status(200).json({ message: 'Inicio de sesión exitoso', usuario: results[0] });
      } else {
        // Si la autenticación falla, envía una respuesta de error
        res.status(401).json({ message: 'Correo electrónico o contraseña incorrectos' });
      }
    });
  });