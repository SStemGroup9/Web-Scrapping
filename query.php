<?php
$name=$_POST["name"];

$db = new SQLite3('facebook_data.db');
$res = $db -> query('SELECT page_id FROM fb_page WHERE name like \'%' . $name . '%\'');
$row = $res->fetchArray(SQLITE3_ASSOC);
$id=$row['page_id'];


$results = $db -> query('SELECT post_date,num_likes FROM posts WHERE page_id=' . $id . ' AND post_date > \'2016-01-01\'');
$data = array();
while ($row = $results->fetchArray(SQLITE3_ASSOC)) {
    $data[] = $row;
}
file_put_contents('result.json',json_encode($data));
#echo json_encode($data);
#header( 'Location: http://student.cs.appstate.edu/yangh1');
?>
