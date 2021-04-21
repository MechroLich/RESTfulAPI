<?php

require_once __DIR__ . '/vendor/autoload.php';
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

$connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
$channel = $connection->channel();
$channel->queue_declare('hello', false, false, false, false);

if(!isset($_REQUEST['date'],
            $_REQUEST['description'],
            $_REQUEST['temperature']))
      return 0;
   //sanitize data

$date = filter_var($_REQUEST['date'], FILTER_SANITIZE_SPECIAL_CHARS);
$description = filter_var($_REQUEST['description'], FILTER_SANITIZE_SPECIAL_CHARS); 
$temp = filter_var($_REQUEST['temperature'], FILTER_SANITIZE_SPECIAL_CHARS);

$msg = new AMQPMessage("from php call Weather for " . $date . " is " . $description . "with temperature of " . (string)$temp);
$channel->basic_publish($msg, '', 'hello');