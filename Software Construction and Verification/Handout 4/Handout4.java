class Logger{
    public static final Logger log = new Logger();

    void write(String message){

    }

    String get(int i){

    }

    int last(){

    }
}

class IndoorLighting extends AbstractRule implements Runnable{

    IndoorLighting(Sensor [] ss,Actuator[] as)
        /@*requires array_slice_deep(ss,0,ss.legth,SensorInv,unit,_,_) &*&
             array_slice_deep(ss,0,as.legth,ActuatorInv,unit,_,_);
             
        @*/
    {

    }

    //@ provides RuleInv(this)
    {
        ...
        //@close RuleInv(this);
    }

    ...{
        //from the Invariant
        //@open RuleInv(this);
        i = 0;
        while(i < n)
        //@ invariant array_slice_deep(ss,ss.length, SensorInv,unit,_,_);

        {
            //@ array_slice_deep_split(ss, i, i+1);
            //@ assert array_slice_deep(ss,i,i+1,SensorInv,unit,_,_);
            //@ assert array_slice_deep(ss,ss.length, SensorInv,unit,_,_);
            //@ array_slice_deep_open(ss,i,i+1,SensorInv,unit,_,_);
            //@ assert SensorInv(ss[i]);

            value = ss[i].get();

            //@assert SensorInv(ss[0]);
            v = ss[0].get();
        }

    }

    void run(){
        if(ss cenas){
            as cenas
            Logger.log.write(name + "LAMP #" + i + "ON");
        }

        while(true){
            Logger.log.get(...);
            System.out.println(message);
            TimeUnit.SECONDS.sleep(REFRESHRATE);
        }
    } 
}


class OfficeHours extends AbstractRule implements Runnable{

    OfficeHours(Sensor [] ss,Actuator[] as){

    }

    void run(){
        if(ss cenas){
            cenas
        }

        while(true){
            Logger.log.get(...);
            System.out.println(message);
            TimeUnit.SECONDS.sleep(REFRESHRATE);
        }
    } 
}

class AutoWindows extends AbstractRule implements Runnable{

    AutoWindows(Sensor [] ss,Actuator[] as){

    }

    void run(){
        if(ss cenas){
            as cenas
            
        }

        while(true){
            Logger.log.get(...);
            System.out.println(message);
            TimeUnit.SECONDS.sleep(REFRESHRATE);
        }
    } 
}

class Rain_Wind_Protection extends AbstractRule implements Runnable{

    Rain_Wind_Protection(Sensor [] ss,Actuator[] as){

    }

    void run(){
        if(ss cenas){
            cenas
        }

        while(true){
            Logger.log.get(...);
            System.out.println(message);
            TimeUnit.SECONDS.sleep(REFRESHRATE);
        }
    } 
}

//@ ActuatorInv();
clas Actuator {

    void set(int x)
    //@ ActuatorsInv(this)
    //@ ActuatorsInv(this)
    {
        
    }

    void get(int x)
    //@ ActuatorsInv(this)
    //@ ActuatorsInv(this)
    {
        
    }
}



class Domotic{
    
    public static void main(String [] args){

            Sensor[] sensors = new Sensor[]{
                new LightSensor("Corner 1"),
                new LightSensor("Corner 2"),
                new LightSensor("Corner 3"),
                new LightSensor("Corner 4"),
                new LightSensor("Outdoor")
            }

            Actuator[] actuators = new Sensor[]{
                new lamp("Big")
            }

            new Thread(new IndoorLighting(sensors,actuators)).start();

    }
}