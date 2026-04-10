CREATE DATABASE IF NOT EXISTS webpeliculasDB;
USE webpeliculasDB;

-- TABLA USUARIOS 
CREATE TABLE Usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombreUsuario VARCHAR(100) NOT NULL,
    correoUsuario VARCHAR(100) NOT NULL UNIQUE,
    contrasenaUsuario VARCHAR(255) NOT NULL
);

-- TABLA PELICULAS (Con cambios, para filtrar mejor luego)
CREATE TABLE Peliculas (
    id_pelicula INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    titulo_originalPelicula VARCHAR(150),
    sinopsis TEXT,
    anio INT,
    actoresPelicula TEXT,
    generoPelicula ENUM('Accion', 'Comedia', 'Drama', 'Ciencia Ficcion', 'Terror', 'Romance', 'Animacion', 'Fantasia', 'Documental', 'Otro') DEFAULT 'Otro',
    idiomaPelicula ENUM('Espanol', 'Ingles', 'Japones', 'Coreano', 'Frances', 'Otro') DEFAULT 'Otro'
);

--  TABLA SERIES 
CREATE TABLE Series (
    id_serie INT AUTO_INCREMENT PRIMARY KEY,
    tituloSerie VARCHAR(150) NOT NULL,
    titulo_originalSerie VARCHAR(150),
    sinopsisSerie TEXT,
    anio_lanzamientoSerie INT,
    temporadasSerie INT DEFAULT 1,
    actoresSerie TEXT,
    generoSerie ENUM('Accion', 'Comedia', 'Drama', 'Ciencia Ficcion', 'Terror', 'Romance', 'Animacion', 'Fantasia', 'Documental', 'Otro') DEFAULT 'Otro',
    idiomaSerie ENUM('Espanol', 'Ingles', 'Japones', 'Coreano', 'Frances', 'Otro') DEFAULT 'Otro'
);

-- TABLA CINES (Nueva)
CREATE TABLE Cines (
    id_cine INT AUTO_INCREMENT PRIMARY KEY,
    nombreCine VARCHAR(100) NOT NULL,
    direccionCine VARCHAR(200),
    ciudadCine VARCHAR(100)
);

-- 5. TABLA COMENTARIOS 
CREATE TABLE Comentarios (
    id_comentario INT AUTO_INCREMENT PRIMARY KEY,
    id_peliculaComentario INT NOT NULL,
    id_usuarioComentario INT NOT NULL,
    calificacionComentario INT NOT NULL CHECK (calificacionComentario BETWEEN 1 AND 5),
    textoComentario TEXT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_peliculaComentario) REFERENCES Peliculas(id_pelicula),
    FOREIGN KEY (id_usuarioComentario) REFERENCES Usuarios(id_usuario)
);

-- TABLA FAVORITOS (nueva)
CREATE TABLE Favoritos (
    id_favorito INT AUTO_INCREMENT PRIMARY KEY,
    id_usuarioFavorito INT NOT NULL,
    id_peliculaFavorito INT NOT NULL,
    fecha_agregado DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuarioFavorito) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_peliculaFavorito) REFERENCES Peliculas(id_pelicula),
    UNIQUE (id_usuarioFavorito, id_peliculaFavorito) 
);

-- TABLA CARTELERAS (Nueva) <-- esta es la tabla transitiva de entre peliculas y cine
CREATE TABLE Carteleras (
    id_cartelera INT AUTO_INCREMENT PRIMARY KEY,
    id_peliculaCartelera INT NOT NULL,
    id_cineCartelera INT NOT NULL,
    fecha_horaCartelera DATETIME NOT NULL,
    idioma_proyeccionCartelera ENUM('Doblada al Espanol', 'Subtitulada', 'Idioma Original') NOT NULL, 
    FOREIGN KEY (id_peliculaCartelera) REFERENCES Peliculas(id_pelicula) ON DELETE CASCADE,
    FOREIGN KEY (id_cineCartelera) REFERENCES Cines(id_cine) ON DELETE CASCADE
);



-- DATOS DE PRUEBA


-- Usuarios 
INSERT INTO Usuarios (nombreUsuario, correoUsuario, contrasenaUsuario) VALUES 
('Carlos Perez', 'carlos@prueba.com', '1234'),
('Ana Gomez', 'ana@prueba.com', '5678');

-- Peliculas 
INSERT INTO Peliculas (titulo, titulo_originalPelicula, sinopsis, anio, actoresPelicula, generoPelicula, idiomaPelicula) VALUES 
('Spider-Man', 'Spider-Man', 'Un joven es picado por una araña y obtiene poderes increíbles', 2002, 'Tobey Maguire, Kirsten Dunst, Willem Dafoe', 'Accion', 'Ingles'),
('Shrek', 'Shrek', 'Un ogro rescata a una princesa con la ayuda de un burro parlante', 2001, 'Mike Myers, Eddie Murphy, Cameron Diaz', 'Animacion', 'Ingles'),
('Rápidos y Furiosos', 'The Fast and the Furious', 'Un policía encubierto se infiltra en el mundo de las carreras callejeras', 2001, 'Vin Diesel, Paul Walker, Michelle Rodriguez', 'Accion', 'Ingles'),
('Interestelar', 'Interstellar', 'Un grupo de exploradores viaja a través de un agujero de gusano en el espacio', 2014, 'Matthew McConaughey, Anne Hathaway, Jessica Chastain', 'Ciencia Ficcion', 'Ingles'),
('Parásitos', 'Gisaengchung', 'Una familia pobre se infiltra en el hogar de una familia rica', 2019, 'Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong', 'Drama', 'Coreano'),
('El Viaje de Chihiro', 'Sen to Chihiro no kamikakushi', 'Una niña queda atrapada en un mundo mágico y debe salvar a sus padres', 2001, 'Rumi Hiiragi, Miyu Irino, Mari Natsuki', 'Animacion', 'Japones'),
('El Conjuro', 'The Conjuring', 'Investigadores paranormales ayudan a una familia aterrorizada por una presencia oscura', 2013, 'Vera Farmiga, Patrick Wilson, Lili Taylor', 'Terror', 'Ingles'),
('Amélie', 'Le Fabuleux Destin d''Amélie Poulain', 'Una joven camarera decide cambiar la vida de las personas que la rodean', 2001, 'Audrey Tautou, Mathieu Kassovitz, Rufus', 'Comedia', 'Frances'),
('El Laberinto del Fauno', 'El Laberinto del Fauno', 'En la España posguerra, una niña descubre un fascinante y peligroso mundo mágico', 2006, 'Ivana Baquero, Sergi López, Maribel Verdú', 'Fantasia', 'Espanol'),
('Vengadores: Endgame', 'Avengers: Endgame', 'Los superhéroes sobrevivientes intentan revertir las acciones de Thanos', 2019, 'Robert Downey Jr., Chris Evans, Mark Ruffalo', 'Accion', 'Ingles');

-- Comentarios 
INSERT INTO Comentarios (id_peliculaComentario, id_usuarioComentario, calificacionComentario, textoComentario) VALUES 
(1, 1, 5, '¡Una obra maestra total, mi infancia!'), 
(2, 2, 4, 'Muy divertida, la banda sonora es genial.'); 

-- Favoritos
INSERT INTO Favoritos (id_usuarioFavorito, id_peliculaFavorito) VALUES 
(1, 1), 
(1, 3), 
(2, 2);

-- Cines 
INSERT INTO Cines (nombreCine, direccionCine, ciudadCine) VALUES 
('Cine Colombia', 'Centro Comercial Terra Plaza', 'Popayán'),
('Royal Films', 'Centro Comercial Campanario', 'Popayán');

-- Carteleras 
INSERT INTO Carteleras (id_peliculaCartelera, id_cineCartelera, fecha_horaCartelera, idioma_proyeccionCartelera) VALUES 
(1, 1, '2026-04-15 15:00:00', 'Doblada al Espanol'), 
(4, 1, '2026-04-15 19:30:00', 'Subtitulada'),       
(5, 2, '2026-04-16 18:00:00', 'Subtitulada'),       
(8, 2, '2026-04-16 20:15:00', 'Idioma Original'),    
(10, 1, '2026-04-17 14:00:00', 'Doblada al Espanol'),
(2, 2, '2026-04-17 16:30:00', 'Doblada al Espanol'); 

-- Estos son los datos de la tabla series
INSERT INTO Series (tituloSerie, titulo_originalSerie, sinopsisSerie, anio_lanzamientoSerie, temporadasSerie, actoresSerie, generoSerie, idiomaSerie) 
VALUES 
('Breaking Bad', 'Breaking Bad', 'Un profesor de química con cáncer terminal se asocia con un exalumno para fabricar y vender metanfetamina para asegurar el futuro de su familia.', 2008, 5, 'Bryan Cranston, Aaron Paul, Anna Gunn', 'Drama', 'Ingles'),
('El juego del calamar', 'Ojingeo Geim', 'Cientos de jugadores endeudados aceptan una extraña invitación para competir en juegos infantiles tradicionales con un premio millonario y consecuencias letales.', 2021, 2, 'Lee Jung-jae, Park Hae-soo, Jung Ho-yeon', 'Drama', 'Coreano'),
('Dark', 'Dark', 'La desaparición de dos niños en un pequeño pueblo alemán expone las dobles vidas y las relaciones rotas entre cuatro familias a través de viajes en el tiempo.', 2017, 3, 'Louis Hofmann, Karoline Eichhorn, Lisa Vicari', 'Ciencia Ficcion', 'Otro'),
('La Casa de Papel', 'La Casa de Papel', 'Un grupo de ladrones muy peculiares y con nombres de ciudades asaltan la Fábrica Nacional de Moneda y Timbre en España para llevar a cabo el atraco perfecto.', 2017, 5, 'Úrsula Corberó, Álvaro Morte, Itziar Ituño', 'Accion', 'Espanol'),
('Ataque a los Titanes', 'Shingeki no Kyojin', 'La humanidad vive encerrada en ciudades amuralladas para protegerse de los Titanes, criaturas gigantes que devoran humanos sin razón aparente.', 2013, 4, 'Yuki Kaji, Yui Ishikawa, Marina Inoue', 'Animacion', 'Japones'),
('The Office', 'The Office', 'Un falso documental que retrata el día a día, las absurdidades y las relaciones de los excéntricos empleados de la empresa papelera Dunder Mifflin.', 2005, 9, 'Steve Carell, Rainn Wilson, John Krasinski', 'Comedia', 'Ingles'),
('Lupin', 'Lupin', 'Inspirado en las clásicas aventuras de Arsène Lupin, el carismático ladrón de guante blanco Assane Diop busca vengar a su padre por una injusticia.', 2021, 3, 'Omar Sy, Ludivine Sagnier, Clotilde Hesme', 'Accion', 'Frances'),
('Stranger Things', 'Stranger Things', 'Tras la desaparición de un niño, un pueblo descubre un misterio que involucra experimentos gubernamentales secretos, fuerzas sobrenaturales y a una niña muy extraña.', 2016, 4, 'Millie Bobby Brown, Finn Wolfhard, Winona Ryder', 'Ciencia Ficcion', 'Ingles'),
('Los Simuladores', 'Los Simuladores', 'Cuatro socios resuelven problemas inéditos de sus clientes montando operativos simulados para engañar a quienes los causan.', 2002, 2, 'Federico D''Elía, Alejandro Fiore, Diego Peretti', 'Comedia', 'Espanol'),
('La maldición de Hill House', 'The Haunting of Hill House', 'A través de flashbacks, se exploran los traumas que persiguen a unos hermanos años después de que abandonaran la antigua mansión embrujada donde crecieron.', 2018, 1, 'Michiel Huisman, Carla Gugino, Victoria Pedretti', 'Terror', 'Ingles');


-- DATOS DE CARTELERA

INSERT INTO Carteleras (id_peliculaCartelera, id_cineCartelera, fecha_horaCartelera, idioma_proyeccionCartelera) VALUES
(3, 1, '2026-04-18 15:00:00', 'Doblada al Espanol'),
(6, 1, '2026-04-18 17:30:00', 'Subtitulada'),
(7, 2, '2026-04-18 20:00:00', 'Doblada al Espanol'),

(9, 2, '2026-04-19 14:00:00', 'Idioma Original'),
(2, 1, '2026-04-19 16:15:00', 'Doblada al Espanol'),
(5, 2, '2026-04-19 18:45:00', 'Subtitulada'),

(8, 1, '2026-04-20 15:30:00', 'Idioma Original'),
(1, 2, '2026-04-20 18:00:00', 'Doblada al Espanol'),
(4, 1, '2026-04-20 20:30:00', 'Subtitulada'),

(10, 2, '2026-04-21 14:00:00', 'Doblada al Espanol'),
(6, 1, '2026-04-21 16:30:00', 'Subtitulada'),
(3, 2, '2026-04-21 19:00:00', 'Doblada al Espanol'),

(7, 1, '2026-04-22 15:00:00', 'Doblada al Espanol'),
(9, 2, '2026-04-22 17:30:00', 'Idioma Original'),
(2, 1, '2026-04-22 20:00:00', 'Doblada al Espanol');