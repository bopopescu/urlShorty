<?php 

$url_name =$_POST['urlname'];
//$url_name = "http://www.slate.com";
// $url = 'http://www.google.com';
//$url = 'http://www.slate.com/articles/health_and_science/medical_examiner/2013/12/millennial_narcissism_helicopter_parents_are_college_students_bigger_problem.html';
 //echo json_encode(get_headers($url));
 
 
 //$tags = get_meta_tags($url);
// echo json_encode($tags);
//echo json_encode($tags);


$html = file_get_contents_curl($url_name);

//parsing begins here:
$doc = new DOMDocument();
@$doc->loadHTML($html);
$nodes = $doc->getElementsByTagName('title');

//get and display what you need:
$title = $nodes->item(0)->nodeValue;

$metas = $doc->getElementsByTagName('meta');

for ($i = 0; $i < $metas->length; $i++)
{
    $meta = $metas->item($i);
    if($meta->getAttribute('name') == 'description')
        $description = $meta->getAttribute('content');
    if($meta->getAttribute('name') == 'keywords')
        $keywords = $meta->getAttribute('content');
}

// echo "Title: $title". '<br/><br/>';
// echo "Description: $description". '<br/><br/>';
// echo "Keywords: $keywords";
$arr = array('title' => $title, 'description' => $description, 'keywords' => $keywords);
//$arr = array('title' => 'one', 'description' => 'two', 'keywords' => 'three');
echo json_encode($arr);

function file_get_contents_curl($url)
{
    $ch = curl_init();

    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);

    $data = curl_exec($ch);
    curl_close($ch);

    return $data;
}


?>