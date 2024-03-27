object DataLoad {
  private def getJsonField(json: JValue, key: String): Option[String] = {
    val value = (json \ key)
    value match {
      case jval: JValue => Some(jval.values.toString)
      case _ => None
    }
  }
  def load(logger: Logger, hiveDatabase: String, hiveTable: String, dw_table_name: String): Unit = {
    val conf = ConfigFactory.load
    val yarnResourceManager = conf.getString("app.yarnResourceManager")
    val sparkExecutors = conf.getString("app.sparkExecutors")
    val sparkHome = conf.getString("app.sparkHome")
    val sparkAppJar = conf.getString("app.sparkAppJar")
    val sparkMainClass = conf.getString("app.sparkMainClass")
    val sparkMaster = conf.getString("app.sparkMaster")
    val sparkDriverMemory = conf.getString("app.sparkDriverMemory")
    val sparkExecutorMemory = conf.getString("app.sparkExecutorMemory")
    var destination = ""
    if(dw_table_name.contains("s3a://")){
      destination = "s3"
    }
    else
      {
        destination = "sql"
      }
  val spark = new SparkLauncher()
    .setSparkHome(sparkHome)
    .setAppResource(sparkAppJar)
    .setMainClass(sparkMainClass)
    .setMaster(sparkMaster)
    .addAppArgs(hiveDatabase)
    .addAppArgs(hiveTable)
    .addAppArgs(destination)
    .setVerbose(false)
    .setConf("spark.driver.memory", sparkDriverMemory)
    .setConf("spark.executor.memory", sparkExecutorMemory)
    .setConf("spark.executor.cores", sparkExecutors)
    .setConf("spark.executor.instances", sparkExecutors)
    .setConf("spark.driver.maxResultSize", "5g")
    .setConf("spark.sql.broadcastTimeout", "144000")
    .setConf("spark.network.timeout", "144000")
    .startApplication()

  var unknownCounter = 0
  while(!spark.getState.isFinal) {
    println(spark.getState.toString)
    Thread.sleep(10000)

    if(unknownCounter > 3000){
      throw new IllegalStateException("Spark Job Failed, timeout expired 8 hours")
    }
    unknownCounter += 1
  }
    println(spark.getState.toString)
    val appId: String = spark.getAppId
    println(s"appId: $appId")
    var finalState = ""
    var i = 0
    while(i < 5){
      val response = Http(s"http://$yarnResourceManager/ws/v1/cluster/apps/$appId/").asString
      if(response.code.toString.startsWith("2"))
      {
        val json = parse(response.body)
        finalState = getJsonField(json \ "app","finalStatus").getOrElse("")
        i = 55
      }
      else {
        i = i+1
      }
    }
    if(finalState.equalsIgnoreCase("SUCCEEDED")){
      println("SPARK JOB SUCCEEDED")
    }
    else {
      throw new IllegalStateException("Spark Job Failed")
    }
  }
}