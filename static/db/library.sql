-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 25, 2023 at 01:05 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `library`
--

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `id` int(11) NOT NULL,
  `names` varchar(200) NOT NULL,
  `bookId` int(11) NOT NULL,
  `address` varchar(200) NOT NULL,
  `phone` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT 0,
  `createdAt` timestamp NOT NULL DEFAULT current_timestamp(),
  `updatedAt` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`id`, `names`, `bookId`, `address`, `phone`, `email`, `status`, `createdAt`, `updatedAt`) VALUES
(1, 'Niyoyita Claude', 1, 'Kigali', '0787467346', 'claud@gmail.com', 1, '2023-04-22 15:27:29', '0000-00-00 00:00:00'),
(3, 'Nizeyimana Jean de Dieu', 4, 'Kigali', '0788800088', 'salima@gmail.com', 0, '2023-04-23 19:46:18', '0000-00-00 00:00:00'),
(4, 'IRERA Aida', 3, 'Kigali', '7453943348', 'jas@gmail.com', 0, '2023-04-23 19:52:38', '0000-00-00 00:00:00'),
(5, 'IRERA Aida', 3, 'Kigali', '7453943348', 'jas@gmail.com', 0, '2023-04-23 19:54:26', '0000-00-00 00:00:00'),
(6, 'Uwingabire Tresor', 3, 'Kigali', '0788800088', 'solange@gmail.com', 1, '2023-04-23 19:54:50', '0000-00-00 00:00:00'),
(7, 'IRERA Tresor', 4, 'Kigali', '0788800088', 'jas@gmail.com', 0, '2023-04-23 20:17:08', '0000-00-00 00:00:00'),
(8, 'sam san', 4, 'mkl', '!234556', 'sa@gmail.com', 0, '2023-04-24 21:08:17', '0000-00-00 00:00:00'),
(9, 'sam san', 4, 'mkl', '!234556', 'sa@gmail.com', 0, '2023-04-24 21:09:02', '0000-00-00 00:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `bookId` int(11) NOT NULL,
  `title` text NOT NULL,
  `auth` varchar(50) NOT NULL,
  `quantity` int(11) NOT NULL,
  `publisher` text NOT NULL,
  `image` text NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT 1,
  `updatedAt` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE current_timestamp(),
  `createdAt` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`bookId`, `title`, `auth`, `quantity`, `publisher`, `image`, `status`, `updatedAt`, `createdAt`) VALUES
(1, 'gfdg', 'dfgd', 2, 'dfgd', 'dfgdg', 0, '2023-04-22 22:49:18', '2023-04-22 14:35:12'),
(3, 'Story of the Wolf', 'Solange', 27, 'Tumba library', 'IPRC TUMBA LOGO.png', 0, '2023-04-24 19:28:22', '2023-04-22 22:33:22'),
(4, 'Adventure book', 'Gtan', 37, 'span across two columns. This effectively merges the second and third columns of the table, allowing the \"Sales\" heading to span both columns', 'IPRC TUMBA LOGO.png', 1, '2023-04-24 22:49:11', '2023-04-22 22:34:31'),
(5, 'Javascript Programming', 'Tresor Akbar', 45, 'Assuming that your images are located in the static uploads folder, and you have set up your Flask app to serve static files, you can use the following code in your template', 'premium_photo-1677567996070-68fa4181775a.avif', 1, '0000-00-00 00:00:00', '2023-04-23 12:06:32'),
(6, 'zxcv', 'cgj', 23, 'gghhj', 'Screenshot 2023-04-10 at 18.12.38.png', 0, '2023-04-24 22:08:47', '2023-04-24 22:08:42'),
(7, 'ghj', 'dfg', 4, 'dsfgh', 'Reg NO Email Address Phone President.png', 0, '2023-04-24 22:18:12', '2023-04-24 22:12:03'),
(8, 'fdghj', 'dfghjn', 2, 'tyuj', 'Screenshot 2023-04-10 at 18.12.38.png', 0, '2023-04-24 22:15:54', '2023-04-24 22:14:02'),
(9, 'dkdsakjskjdakjkas', 'jon', 4, 'sdjfkajsdkfa\r\nsdkfjwk\r\nekjwjew', 'Reg NO Email Address Phone President.png', 0, '2023-04-24 22:51:48', '2023-04-24 22:51:14');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `fname` varchar(200) NOT NULL,
  `lname` varchar(255) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `profile` varchar(255) NOT NULL DEFAULT 'profile.png',
  `pid` varchar(16) NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT 1,
  `createdAt` timestamp NOT NULL DEFAULT current_timestamp(),
  `updatedAt` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `fname`, `lname`, `username`, `password`, `profile`, `pid`, `status`, `createdAt`, `updatedAt`) VALUES
(1, 'Nizeyimana', 'Jean de Dieu', 'jado@gmail.com', 'pbkdf2:sha256:260000$k03HXaodirO0yzi1$d9ec44de9f7649afe8dfbdb22e7c3274d14ce57be1db34ba7ea276e7956c110b', 'profile.png', '1199880055773388', 1, '2023-04-22 12:54:02', '0000-00-00 00:00:00'),
(3, 'Habimana', 'Aime Tresor', 'tresor@gmail.com', 'pbkdf2:sha256:260000$qwAgmWnFfdohXgUy$8e1ed8c889076b07810c9d9ba3e01f44f8eb2b957c5da8fdb2ec9fbb81d1ac46', 'profile.png', '1199880055773381', 1, '2023-04-22 12:56:08', '2023-04-24 19:54:19'),
(6, 'Nizeyimana', 'Jean de Dieu', 'salima@gmail.com', 'pbkdf2:sha256:260000$7ofNM8H8JXXtoTrj$68c01145ece9c6f477fd3d00e4e2eb1d7345dac809023384ca545424eb5d1ece', 'profile.png', '120003003398980', 0, '2023-04-22 13:38:59', '0000-00-00 00:00:00'),
(8, 'Nizeyimana', 'Aida', 'jas@gmail.com', 'pbkdf2:sha256:260000$Wy0XGUOdqELv6dhP$19a224ec2c74a42a35d56bb21e44cf8923b66359d4186ca69ad048f22998af80', 'profile.png', '120003003398987', 0, '2023-04-22 13:50:04', '0000-00-00 00:00:00'),
(10, 'Uwingabire', 'Solange', 'solange@gmail.com', 'pbkdf2:sha256:260000$B37QeoJQUJDkfwfL$f5ed749c71b8452aa2cff2eddf4e83a631abdf9493df09d3c7243420f926263e', 'profile.png', '1200030033989800', 1, '2023-04-22 13:51:46', '0000-00-00 00:00:00'),
(11, 'Trial', 'Aida', 'cyizalandry5@gmail.com', 'pbkdf2:sha256:260000$NmvL5vz9tVGJOIQW$768f5d10ad4cb70875bb23c14d29bc1b36576afbb9d936369ea6775536a01d5e', 'profile.png', '1139880055773388', 1, '2023-04-24 19:55:04', '0000-00-00 00:00:00'),
(13, 'Uwingabire', 'Name', 'jaso@gmail.com', 'pbkdf2:sha256:260000$0Eyfc8FTUMtrMpDv$ee8ad5685e139cd6a9a81b153a7c8a966abfb92171de3b3408c2e82dfca19166', 'profile.png', '119980055773388', 0, '2023-04-24 19:56:38', '0000-00-00 00:00:00');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bookId` (`bookId`);

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`bookId`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user` (`username`),
  ADD UNIQUE KEY `pid` (`pid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `bookId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`bookId`) REFERENCES `books` (`bookId`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
