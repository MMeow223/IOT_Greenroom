-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 25, 2023 at 08:55 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `iot_greenroom`
--

-- --------------------------------------------------------

--
-- Table structure for table `air_moisture_actuator_activity`
--

CREATE TABLE `air_moisture_actuator_activity` (
  `id` int(11) NOT NULL,
  `action` varchar(255) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `greenroom_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `air_moisture_sensor`
--

CREATE TABLE `air_moisture_sensor` (
  `id` int(11) NOT NULL,
  `value` decimal(10,2) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `greenroom_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `greenroom`
--

CREATE TABLE `greenroom` (
  `greenroom_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `location` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `greenroom`
--

INSERT INTO `greenroom` (`greenroom_id`, `name`, `location`, `description`) VALUES
(1, 'GreenRoom1', 'Lab', 'This is greenroom 1'),
(2, 'Greenroom2', 'House', 'This is Greenroom 2');

-- --------------------------------------------------------

--
-- Table structure for table `light_actuator_activity`
--

CREATE TABLE `light_actuator_activity` (
  `id` int(11) NOT NULL,
  `action` varchar(255) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `greenroom_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `light_sensor`
--

CREATE TABLE `light_sensor` (
  `id` int(11) NOT NULL,
  `value` decimal(10,2) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `greenroom_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `light_sensor`
--

INSERT INTO `light_sensor` (`id`, `value`, `timestamp`, `greenroom_id`) VALUES
(1, 41.00, '2023-10-25 18:00:16', 2),
(2, 41.00, '2023-10-25 18:00:19', 2),
(3, 41.00, '2023-10-25 18:00:25', 2),
(4, 41.00, '2023-10-25 18:00:25', 2),
(5, 41.00, '2023-10-25 18:00:25', 2),
(6, 41.00, '2023-10-25 18:00:25', 2),
(7, 41.00, '2023-10-25 18:00:26', 2),
(8, 41.00, '2023-10-25 18:00:26', 2),
(9, 41.00, '2023-10-25 18:00:26', 2),
(10, 41.00, '2023-10-25 18:00:26', 2),
(11, 41.00, '2023-10-25 18:00:26', 2),
(12, 41.00, '2023-10-25 18:00:26', 2),
(13, 41.00, '2023-10-25 18:00:27', 2);

-- --------------------------------------------------------

--
-- Table structure for table `soil_moisture_actuator_activity`
--

CREATE TABLE `soil_moisture_actuator_activity` (
  `id` int(11) NOT NULL,
  `action` varchar(255) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `greenroom_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `soil_moisture_sensor`
--

CREATE TABLE `soil_moisture_sensor` (
  `id` int(11) NOT NULL,
  `value` decimal(10,2) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `greenroom_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `soil_moisture_sensor`
--

INSERT INTO `soil_moisture_sensor` (`id`, `value`, `timestamp`, `greenroom_id`) VALUES
(1, 10.00, '2023-10-23 09:20:33', 1),
(2, 21.00, '2023-10-24 12:51:58', 1),
(3, 21.00, '2023-10-24 12:52:02', 1),
(4, 21.00, '2023-10-24 12:52:10', 1),
(5, 21.00, '2023-10-24 12:52:11', 1),
(6, 21.00, '2023-10-24 12:52:12', 1),
(7, 33.00, '2023-10-24 12:52:27', 1),
(8, 21.00, '2023-10-24 12:52:12', 1),
(9, 21.00, '2023-10-24 12:52:12', 1),
(10, 21.00, '2023-10-24 12:52:12', 1),
(11, 55.00, '2023-10-24 12:52:31', 1),
(12, 21.00, '2023-10-24 12:52:13', 1),
(13, 21.00, '2023-10-24 12:52:13', 1),
(14, 21.00, '2023-10-24 12:52:13', 1),
(15, 21.00, '2023-10-24 12:52:13', 1),
(16, 21.00, '2023-10-24 12:52:14', 1),
(17, 21.00, '2023-10-24 12:52:14', 1),
(18, 21.00, '2023-10-24 12:52:14', 1),
(19, 21.00, '2023-10-24 12:52:14', 1),
(20, 21.00, '2023-10-24 12:52:14', 1),
(21, 21.00, '2023-10-24 12:52:14', 1),
(22, 21.00, '2023-10-24 12:52:15', 1),
(23, 21.00, '2023-10-24 12:52:15', 1),
(24, 21.00, '2023-10-24 12:52:15', 1),
(25, 21.00, '2023-10-24 12:52:15', 1),
(26, 21.00, '2023-10-24 12:52:15', 1),
(27, 21.00, '2023-10-24 12:52:15', 1),
(28, 21.00, '2023-10-25 18:16:14', 1),
(29, 21.00, '2023-10-25 18:16:27', 2),
(30, 21.00, '2023-10-25 18:16:30', 1),
(31, 21.00, '2023-10-25 18:16:22', 2),
(32, 21.00, '2023-10-25 18:16:24', 1),
(33, 21.00, '2023-10-25 18:16:17', 1),
(34, 21.00, '2023-10-25 18:16:20', 2);

-- --------------------------------------------------------

--
-- Table structure for table `temperature_actuator_activity`
--

CREATE TABLE `temperature_actuator_activity` (
  `id` int(11) NOT NULL,
  `action` varchar(255) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `greenroom_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `temperature_sensor`
--

CREATE TABLE `temperature_sensor` (
  `id` int(11) NOT NULL,
  `value` decimal(5,2) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `greenroom_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `water_level_actuator_activity`
--

CREATE TABLE `water_level_actuator_activity` (
  `id` int(11) NOT NULL,
  `action` varchar(255) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `greenroom_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `water_level_sensor`
--

CREATE TABLE `water_level_sensor` (
  `id` int(11) NOT NULL,
  `value` decimal(10,2) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `greenroom_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `air_moisture_actuator_activity`
--
ALTER TABLE `air_moisture_actuator_activity`
  ADD PRIMARY KEY (`id`),
  ADD KEY `greenroom_id` (`greenroom_id`);

--
-- Indexes for table `air_moisture_sensor`
--
ALTER TABLE `air_moisture_sensor`
  ADD PRIMARY KEY (`id`),
  ADD KEY `greenroom_id` (`greenroom_id`);

--
-- Indexes for table `greenroom`
--
ALTER TABLE `greenroom`
  ADD PRIMARY KEY (`greenroom_id`);

--
-- Indexes for table `light_actuator_activity`
--
ALTER TABLE `light_actuator_activity`
  ADD PRIMARY KEY (`id`),
  ADD KEY `greenroom_id` (`greenroom_id`);

--
-- Indexes for table `light_sensor`
--
ALTER TABLE `light_sensor`
  ADD PRIMARY KEY (`id`),
  ADD KEY `greenroom_id` (`greenroom_id`);

--
-- Indexes for table `soil_moisture_actuator_activity`
--
ALTER TABLE `soil_moisture_actuator_activity`
  ADD PRIMARY KEY (`id`),
  ADD KEY `greenroom_id` (`greenroom_id`);

--
-- Indexes for table `soil_moisture_sensor`
--
ALTER TABLE `soil_moisture_sensor`
  ADD PRIMARY KEY (`id`),
  ADD KEY `greenroom_id` (`greenroom_id`);

--
-- Indexes for table `temperature_actuator_activity`
--
ALTER TABLE `temperature_actuator_activity`
  ADD PRIMARY KEY (`id`),
  ADD KEY `greenroom_id` (`greenroom_id`);

--
-- Indexes for table `temperature_sensor`
--
ALTER TABLE `temperature_sensor`
  ADD PRIMARY KEY (`id`),
  ADD KEY `greenroom_id` (`greenroom_id`);

--
-- Indexes for table `water_level_actuator_activity`
--
ALTER TABLE `water_level_actuator_activity`
  ADD PRIMARY KEY (`id`),
  ADD KEY `greenroom_id` (`greenroom_id`);

--
-- Indexes for table `water_level_sensor`
--
ALTER TABLE `water_level_sensor`
  ADD PRIMARY KEY (`id`),
  ADD KEY `greenroom_id` (`greenroom_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `air_moisture_actuator_activity`
--
ALTER TABLE `air_moisture_actuator_activity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `air_moisture_sensor`
--
ALTER TABLE `air_moisture_sensor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `greenroom`
--
ALTER TABLE `greenroom`
  MODIFY `greenroom_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `light_actuator_activity`
--
ALTER TABLE `light_actuator_activity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `light_sensor`
--
ALTER TABLE `light_sensor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `soil_moisture_actuator_activity`
--
ALTER TABLE `soil_moisture_actuator_activity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `soil_moisture_sensor`
--
ALTER TABLE `soil_moisture_sensor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `temperature_actuator_activity`
--
ALTER TABLE `temperature_actuator_activity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `temperature_sensor`
--
ALTER TABLE `temperature_sensor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `water_level_actuator_activity`
--
ALTER TABLE `water_level_actuator_activity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `water_level_sensor`
--
ALTER TABLE `water_level_sensor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `air_moisture_actuator_activity`
--
ALTER TABLE `air_moisture_actuator_activity`
  ADD CONSTRAINT `air_moisture_actuator_activity_ibfk_1` FOREIGN KEY (`greenroom_id`) REFERENCES `greenroom` (`greenroom_id`);

--
-- Constraints for table `air_moisture_sensor`
--
ALTER TABLE `air_moisture_sensor`
  ADD CONSTRAINT `air_moisture_sensor_ibfk_1` FOREIGN KEY (`greenroom_id`) REFERENCES `greenroom` (`greenroom_id`);

--
-- Constraints for table `light_actuator_activity`
--
ALTER TABLE `light_actuator_activity`
  ADD CONSTRAINT `light_actuator_activity_ibfk_1` FOREIGN KEY (`greenroom_id`) REFERENCES `greenroom` (`greenroom_id`);

--
-- Constraints for table `light_sensor`
--
ALTER TABLE `light_sensor`
  ADD CONSTRAINT `light_sensor_ibfk_1` FOREIGN KEY (`greenroom_id`) REFERENCES `greenroom` (`greenroom_id`);

--
-- Constraints for table `soil_moisture_actuator_activity`
--
ALTER TABLE `soil_moisture_actuator_activity`
  ADD CONSTRAINT `soil_moisture_actuator_activity_ibfk_1` FOREIGN KEY (`greenroom_id`) REFERENCES `greenroom` (`greenroom_id`);

--
-- Constraints for table `soil_moisture_sensor`
--
ALTER TABLE `soil_moisture_sensor`
  ADD CONSTRAINT `soil_moisture_sensor_ibfk_1` FOREIGN KEY (`greenroom_id`) REFERENCES `greenroom` (`greenroom_id`);

--
-- Constraints for table `temperature_actuator_activity`
--
ALTER TABLE `temperature_actuator_activity`
  ADD CONSTRAINT `temperature_actuator_activity_ibfk_1` FOREIGN KEY (`greenroom_id`) REFERENCES `greenroom` (`greenroom_id`);

--
-- Constraints for table `temperature_sensor`
--
ALTER TABLE `temperature_sensor`
  ADD CONSTRAINT `temperature_sensor_ibfk_1` FOREIGN KEY (`greenroom_id`) REFERENCES `greenroom` (`greenroom_id`);

--
-- Constraints for table `water_level_actuator_activity`
--
ALTER TABLE `water_level_actuator_activity`
  ADD CONSTRAINT `water_level_actuator_activity_ibfk_1` FOREIGN KEY (`greenroom_id`) REFERENCES `greenroom` (`greenroom_id`);

--
-- Constraints for table `water_level_sensor`
--
ALTER TABLE `water_level_sensor`
  ADD CONSTRAINT `water_level_sensor_ibfk_1` FOREIGN KEY (`greenroom_id`) REFERENCES `greenroom` (`greenroom_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
