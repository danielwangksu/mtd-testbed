<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>ABC :: Build Your Network</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link href="css/style.css" rel="stylesheet" type="text/css" />
<link rel="SHORTCUT ICON" href="imaginiSite/favicon.ico" type="image/x-icon"> 
</head>

<body bgcolor = "lightblue">
<center>
<table>
<!--<tr>
<td> 
<script language="JavaScript" type="text/javascript">

		function random_img(){
  		var imaginiSite=new Array()
		  imaginiSite[1]="4.jpg"
		  imaginiSite[2]="5.jpg"
		  imaginiSite[3]="6.jpg"
  var randimg = Math.floor(Math.random() * imaginiSite.length)

  if (randimg==0)
  {
	randimg=1
  }
	
  document.write('<img src="imaginiSite/' + imaginiSite[randimg] + '"  alt="Codex" width="630" height="172"/>')
}

  random_img()

</script> 
</td>
</tr>-->
</table>

<?php

function createSwitch ($fh, $switchName, $networkName){
	$switch = "create-vSwitch \$esxi \"$switchName\" \"$networkName\" \n";
	fwrite($fh, $switch);
	return true;
}

function createVM($fh, $VMname, $template, $NICs, $networkSeg){
	$crVM = "createVM \$esxi \"$VMname\" \"$template\" \$datastore \n";
	switch ($networkSeg){
		case "perimeterSC":
			$NIC = "configNIC \"$VMname\" $NICs \"N127 Physical Network\" \"a-switch1\" \"a-switch2\" \n";
			break;	
		
		case "perimeterS":
			$NIC = "configNIC \"$VMname\" $NICs \"N127 Physical Network\" \"a-switch1\" \n";
			break;	
		
		case "perimeterC":
			$NIC = "configNIC \"$VMname\" $NICs \"N127 Physical Network\" \"a-switch2\" \n";
			break;	
		
		case "server":
			$NIC = "configNIC \"$VMname\" $NICs \"a-switch1\" \n";
			break;
		
		case "intISC":
			$NIC = "configNIC \"$VMname\" $NICs \"a-switch2\" \"a-switch3\" \"a-switch4\" \n";
			break;
		
		case "intC":
			$NIC = "configNIC \"$VMname\" $NICs \"a-switch2\" \"a-switch3\" \n";
			break;
		
		case "intIS":
			$NIC = "configNIC \"$VMname\" $NICs \"a-switch2\" \"a-switch4\" \n";
			break;
			
		case "intServer":
			$NIC = "configNIC \"$VMname\" $NICs \"a-switch4\" \n";
			break;
		
		case "client":
			$NIC = "configNIC \"$VMname\" $NICs \"a-switch3\" \n";
			break;
	}
		
	fwrite($fh, $crVM);
	fwrite($fh, $NIC);
	//fwrite($fh, "start-VM \"$VMname\" \n");
}

$submit = $_POST['submit'];

if($submit){

	$webNo = $_POST['webNo']; //echo "total web = $webNo <br />";
	$opWeb = $_POST['opWeb']; //echo "Apche = $opWeb <br />";
	$opWeb1 = $_POST['opWeb1']; //echo "IIS = $opWeb1 <br />";
	$confWeb = $_POST['confWeb']; //echo "websubnet = $confWeb <br />";
	$confWeb1 = $_POST['confWeb1'];	//echo "other web subnet = $confWeb1 <br />";
	$confWeb2 = $_POST['confWeb2'];	//echo "total no server = $confWeb2 <br />";
	$mailNo = $_POST['mailNo']; //echo "total mail = $mailNo <br />";
	$opMail = $_POST['opMail']; //echo " Exchange = $opMail <br />";
	$opMail1 = $_POST['opMail1']; //echo " other = $opMail1 <br />";
	$confMail = $_POST['confMail']; //echo "mail subnet = $confMail <br />";
	$confMail1 = $_POST['confMail1']; //echo "mail subnet = $confMail1 <br />";
	$confMail2 = $_POST['confMail2']; //echo "other mail subnet = $confMail2 <br />";
	$logNo = $_POST['logNo']; //echo "total log = $logNo <br />";
	$opLog = $_POST['opLog']; //echo "Splunk = $opLog <br />";
	$opLog1 = $_POST['opLog1']; //echo "other = $opLog1 <br />";
	$confLog = $_POST['confLog']; //echo "log subnet = $confLog <br />";
	$confLog1 = $_POST['confLog1']; //echo "other log subnet = $confLog1 <br />";
	$confLog2 = $_POST['confLog2']; //echo "total no server = $confLog2 <br />";
	$fileNo = $_POST['fileNo']; //echo "total no server = $fileNo <br />";
	$opFile = $_POST['opFile']; //echo "total no server = $opFile <br />";
	$opFile1 = $_POST['opFile1']; //echo "total no server = $opFile1 <br />";
	$confFile = $_POST['confFile']; //echo "total no server = $confFile <br />";
	$confFile1 = $_POST['confFile1']; //echo "total no server = $confFile1 <br />";
	$confFile2 = $_POST['confFile2']; //echo "total no server = $confFile2 <br />";
	$vpnNo = $_POST['vpnNo']; //echo "total no server = $vpnNo <br />";
	$opVpn1 = $_POST['opVpn1']; //echo "total no server = $opVpn1 <br />";
	$confVpn = $_POST['confVpn']; //echo "total no server = $confVpn <br />";
	$confVpn1 = $_POST['confVpn1']; //echo "total no server = $confVpn1 <br />";
	$confVpn2 = $_POST['confVpn2']; //echo "total no server = $confVpn2 <br />";
	$clientNo = $_POST['clientNo']; //echo "total no server = $clientNo <br />";
	$opClient = $_POST['opClient']; //echo "total no server = $opClient <br />";
	$opClient1 = $_POST['opClient1']; //echo "total no server = $opClient1 <br />";
	//$opClient2 = $_POST['opClient2']; //echo "total no server = $opClient2 <br />";
	$confClient = $_POST['confClient']; //echo "total no server = $confClient <br />";
	$confClient1 = $_POST['confClient1']; //echo "total no server = $confClient1 <br />";
	$confClient2 = $_POST['confClient2']; //echo "total no server = $confClient2 <br />";
	
	echo $confClient;
	
	$myFile = "network.ps1";
	$fh = fopen($myFile, 'w') or die("can't open file");
	
	$workaround = "\$bindingFlags = [Reflection.BindingFlags] \"Instance,NonPublic,GetField\" \n" +
				  "\$objectRef = \$host.GetType().GetField(\"externalHostRef\", \$bindingFlags).GetValue(\$host) \n" +
				  "\$bindingFlags = [Reflection.BindingFlags] \"Instance,NonPublic,GetProperty\" \n" +
				  "\$consoleHost = \$objectRef.GetType().GetProperty(\"Value\", \$bindingFlags).GetValue(\$objectRef, @()) \n" +
				  "[void] \$consoleHost.GetType().GetProperty(\"IsStandardOutputRedirected\", \$bindingFlags).GetValue(\$consoleHost, @()) \n" +
				  "\$bindingFlags = [Reflection.BindingFlags] \"Instance,NonPublic,GetField\" \n" +
				  "\$field = \$consoleHost.GetType().GetField(\"standardOutputWriter\", \$bindingFlags) \n" +
				  "\$field.SetValue(\$consoleHost, [Console]::Out) \n" +
				  "\$field2 = \$consoleHost.GetType().GetField(\"standardErrorWriter\", \$bindingFlags) \n" +
				  "\$field2.SetValue(\$consoleHost, [Console]::Out)";
	
	//fwrite($fh, $workaround);
	
	$functions = file_get_contents('functions.txt'); 
	fwrite($fh, $functions);
	
	$importPowerCLI = "\nadd-pssnapin VMware.VimAutomation.Core\n";
	fwrite($fh, $importPowerCLI);
	
	$connectData = "Connect-VIServer -Server 192.168.1.15 -Protocol https -User ian -Password ccdc2013!\n";
	fwrite($fh, $connectData);
	
	$hostData = "\$esxi = \"192.168.1.142\" \n\$datastore = \"superComp-HDD\"\n";
	fwrite($fh, $hostData);
	
	$switch1Exists = false;
	if ($webNo || $mailNo){
		$switch1Exists = createSwitch($fh, "a-switch1", "a-switch1");
	}
	
	$switch2Exists = false;
	if ($vpnNo || $clientNo || $logNo || $fileNo){
		$switch2Exists = createSwitch($fh, "a-switch2", "a-switch2");
	}
	
	$switch3Exists = false;
	if ($vpnNo || $clientNo || 1){
		$switch3Exists = createSwitch ($fh, "a-switch3", "a-switch3");
	}
	
	$switch4Exists = false;
	if ($logNo || $fileNo){
		$switch4Exists = createSwitch ($fh, "a-switch4", "a-switch4");
	}
	
	//create FWs with NICs
	if($switch1Exists){
		if ($switch2Exists){
			createVM($fh, "a-pFW", "mtd-pFW-key", 3, perimeterSC);  //create perimeter FW
			
			//create internal FW
			if($switch3Exists && $switch4Exists)
				createVM($fh, "a-intFW", "mtd-intFW-key", 3, intISC);

			if ($switch3Exists && !$switch4Exists)
				createVM($fh, "a-intFW", "mtd-intFW-key", 2, intC);
				
			if (!$switch3Exists && $switch4Exists)
				createVM($fh, "a-intFW", "mtd-intFW-key", 2, intIS);
			
		}
		else 
			createVM($fh, "a-pFW", "mtd-pFW-key", 2, perimeterS);
	}
	else{
		if ($switch2Exists){ 
			createVM($fh, "a-pFW", "mtd-pFW-key", 2, perimeterC);
			
			if($switch3Exists && $switch4Exists)
				createVM($fh, "a-intFW", "mtd-intFW-key", 3, intISC);

			if ($switch3Exists && !$switch4Exists)
				createVM($fh, "a-intFW", "mtd-intFW-key", 2, intC);
				
			if (!$switch3Exists && $switch4Exists)
				createVM($fh, "a-intFW", "mtd-intFW-key", 2, intIS);
		}
	}
	//start a-pFW and intFW
	fwrite($fh, "start-VM \"a-pFW\" \n");
	fwrite($fh, "start-VM \"a-intFW\" \n");
	
	//create the controller and start it
	createVM($fh, "a-mtd-controller", "a-mtd-controller-key-updated", 1, client);	
	fwrite($fh, "start-VM \"a-mtd-controller\" \n");
	
	$serverArray = array();
	
	//create webserver
	if($webNo > 0){
		for ($i = 0; $i < $webNo; $i++){
			createVM($fh, "a-web$i", "mtd-webServerTemplate", 1, server);
			$serverArray[] = "a-web$i";
		}
			
	}
	
	//create mailserver and AD
	if($mailNo > 0){
		createVM($fh, "AD", "mtd-ActiveDir", 1, server);
			
		for ($i = 0; $i < $mailNo; $i++){
			createVM($fh, "mail$i", "mtd-Microsoft_Exchange_Server", 1, server);	
		}
			
	}
	
	//create log servers
	if($logNo > 0){
		for ($i = 0; $i < $logNo; $i++){
			createVM($fh, "log$i", "mtd-loggingServer", 1, intServer);	
		}	
	}
	
	//create file servers
	if($fileNo > 0){
		for ($i = 0; $i < $fileNo; $i++){
			createVM($fh, "file$i", "mtd-NFS_server", 1, intServer);	
		}	
	}
	
	//create vpn server
	if($vpnNo > 0){
		for ($i = 0; $i < $vpnNo; $i++){
			createVM($fh, "vpn$i", "mtd-vpnServer", 1, client);	
		}	
	}
	
	//create client hosts
	if($clientNo > 0){
		for ($i = 0; $i < $opClient; $i++)
			createVM($fh, "a-client$i", "mtd-LinuxMint_client", 1, client);
		for ($j = $i; $j < ($opClient1 + $i); $j++)
			createVM($fh, "a-client$j", "mtd-CentOS_client", 1, client);	
	}
	
	fclose($fh);
	
	//shell_exec('powershell.exe -command C:\wamp\www\mtd\network.ps1 > C:\wamp\www\mtd\network.txt 2>&1');
	//echo "$output";	
	
	//create a file for storing servers information (MAC etc.)
	$myFile1 = "getMAC.ps1";
	$fhs = fopen($myFile1, 'w') or die("can't open file");
	
	//fwrite($fhs, $workaround);
	
	$importPowerCLI = "add-pssnapin VMware.VimAutomation.Core\n";
	fwrite($fhs, $importPowerCLI);
	
	$connectData = "Connect-VIServer -Server 192.168.1.15 -Protocol https -User ian -Password ccdc2013!\n";
	fwrite($fhs, $connectData);
	
	foreach($serverArray as $key => $value){
		fwrite($fhs, "get-networkadapter -vm \"$value\"". "\n");
	}
	fclose($fhs);
	
	shell_exec('powershell.exe -command C:\wamp\www\mtd\onRemoteHost.ps1');


} 

else {

	if($_GET['s'] == 'submit'){
		echo "<form method=\"post\" action=\"index.php?s=submit\">";
	} 

	else { 
		echo "<form method=\"post\" action=\"index.php\">";
	}

?>

<br>
<table border="1">
<tr bgcolor = "orange">
<td width = "100" align = "center"><strong>&nbsp; Services</strong></td>
<td width = "100" align = "center"><strong>&nbsp; Total Number</strong></td>
<td width = "100" align = "center"><strong>&nbsp; Options</strong></td>
</tr>

<tr>
<td width = "100">&nbsp; Web Server</td>
<td width = "115"><center><input type="text" name="webNo" size="1" value="0" /></center></td>
<td width = "150"><input type="text" name="opWeb" size="1" value="" /> Apache (default) <br> 
				<!--  <input type="text" name="opWeb1" size="1" value="-" /> - </td>
				  <input type="radio" name="confWeb1" size="1" value="specify subnet" /><input type="text" name="confWeb2" size="15" value="specify subnet" /> --></td>

</tr>
<!-- <tr>
<td width = "100">&nbsp; Mail Server</td>
<td width = "100"><center><input type="text" name="mailNo" size="1" value="0" /></center></td>
<td width = "250"><input type="text" name="opMail" size="1" value="" /> Exchange-requires AD (default) <br> 
				  <input type="text" name="opMail1" size="1" value="-" /> - </td>
 </td>
</tr> 
<tr>
<td width = "100">&nbsp; Logging Server</td>
<td width = "100"><center><input type="text" name="logNo" size="1" value="0" /></center></td>
<td width = "150"><input type="text" name="opLog" size="1" value="" /> Splunk (default) <br> 
				  <input type="text" name="opLog1" size="1" value="-" /> - </td> </td>

</tr>
<tr>
<td width = "100">&nbsp; File Server</td>
<td width = "100"><center><input type="text" name="fileNo" size="1" value="0" /></center></td>
<td width = "150"><input type="text" name="opFile" size="1" value="" /> NFS (default) <br> 
				  <input type="text" name="opFile1" size="1" value="-" /> - </td></td>

</tr>
<tr>
<td width = "100">&nbsp; VPN Server</td>
<td width = "100"><center><input type="text" name="vpnNo" size="1" value="0" /></center></td>
<td width = "150"><input type="text" name="opVpn" size="1" value="" /> OpenVPN (default) <br> 
				  <input type="text" name="opVpn1" size="1" value="-" /> - </td>
</td>
</tr>	-->			  
<tr>
<td width = "135">&nbsp; Client Workstations</td>
<td width = "100"><center><input type="text" name="clientNo" size="1" value="0" /></center></td>
<td width = "150"><input type="text" name="opClient" size="1" value="" /> Linux Mint 13<br> 
				  <input type="text" name="opClient1" size="1" value="" /> CentOS 6 <br>
<!--<td width = "300"><input type="radio" name="confClient" size="1" value="default" />on 172.17.3.X subnet (default) <br> 
				  <input type="radio" name="confClient" size="1" value="default" />on 192.168.3.X subnet
				  <input type="radio" name="confClient1" size="1" value="specify subnet" /><input type="text" name="confClient2" size="15" value="specify subnet" /> --> </td>
</tr>
</table>
<br>
<!--<table border="1">
<tr bgcolor = "orange">
<td width = "515" align = "center"><strong>&nbsp; Subnets Used in the Network</strong></td>
</tr>
<tr>
<td width = "500"><input type="radio" name="conf" size="1" value="default" />on 172.17.1-3.X subnet (default) <br> 
				  <input type="radio" name="conf" size="1" value="default" />on 192.168.1-3.X subnet <br>
				  <input type="radio" name="conf" size="1" value="default" />on 10.0.1-3.X subnet</td> 
</tr>
</table> -->
<input type="submit" name="submit" value="Submit Configuration" />

<?php
}
?>

</form>

</center>
</body>

</html>