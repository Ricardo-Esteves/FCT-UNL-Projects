import java.util.Random;
import java.util.concurrent.*;
import java.util.concurrent.locks.*;

/*@ 
    	predicate_ctor Sensor_shared_state (SensorInt s) () =
        	s.max |-> ?M &*& s.min |-> ?m &*& s.value |-> ?v &*& v <= M &*& v >= m;
@*/


/*@ 
	predicate SensorInv(SensorInt s) = 
		s.mon |-> ?l &*&
    		l != null &*&
    		lck(l,1,Sensor_shared_state(s));
@*/

class SensorInt {

	int value;
	int min;
	int max;
	ReentrantLock mon;
	
	Thread th;
	
	SensorInt (int min, int max) 
	//@ requires [_]System_out(?o) &*& o != null &*& [_]TimeUnit_SECONDS(?s) &*& s != null &*& max > min;
	//@ ensures SensorInv(this);
	{
		this.min = min;
		this.max = max;
		this.value = min;
		//@ close Sensor_shared_state(this)();
      		//@ close enter_lck(1,Sensor_shared_state(this));
		mon = new ReentrantLock();
		//@ close SensorInv(this);
		this.th = new Thread(new Probe(this));
		this.th.start();
		
	}
	
	int get() 
	//@ requires SensorInv(this);
	//@ ensures SensorInv(this);
	{
		int v;
      		//@ open SensorInv(this);
      		mon.lock(); 
      		//@ open Sensor_shared_state(this)();
      		v = this.value; 
      		//@ close Sensor_shared_state(this)();
      		mon.unlock();	
      		//@ close SensorInv(this);
      		return v; 
	}
	
	void set (int value) 
	//@ requires SensorInt_value(this, _) &*& SensorInv(this);
	//@ ensures SensorInv(this);
	{ 
		//@ open SensorInv(this);
		mon.lock();
		//@ open Sensor_shared_state(this)();
		this.value = value;
		//@ close Sensor_shared_state(this)(); 
		mon.unlock();
		//@ close SensorInv(this);	
	}
	
	public static void main (String args[]) 
		throws InterruptedException /*@ ensures true; @*/
		//@ requires [_]System_out(?o) &*& o != null &*& [_]TimeUnit_SECONDS(?s) &*& s != null;
		//@ ensures true;
		
		{
		SensorInt sensor = new SensorInt(0,10);
		while (true)
		
		/*@ invariant
		    [_]System_out(?p) &*& p != null &*&
		    [_]TimeUnit_SECONDS(?t) &*& t != null;
		@*/
		
		{
		
			TimeUnit.SECONDS.sleep(5);
			
			
			System.out.println("Sensors read: " + Integer.toString(sensor.get()));
			
		}
	}
}

/*@ 
	predicate ProbeInv(Probe k;) = 
		[_]System_out(?o) &*& o != null &*& 
		[_]TimeUnit_SECONDS(?s) &*& s != null &*&
		k.sensor |-> ?j &*& j != null ;
@*/

class Probe implements Runnable {

	//@ predicate pre() = ProbeInv(this);
	//@ predicate post() = true;

	private SensorInt sensor;
	
	public Probe (SensorInt sensor)
	/*@ requires [_]System_out(?o) &*& o != null &*& 
		[_]TimeUnit_SECONDS(?s) &*& 
		s != null &*& sensor != null &*& 
		[_]SensorInv(sensor);
	@*/
	//@ ensures pre();
	{ 
		this.sensor = sensor;
		//@ close pre();	
	}
	
	public void run()
	//@ requires pre();
	//@ ensures post();
	{
		Random r = new Random ();
		int valueProduced;
		while( true )
		/*@ invariant
		    [_]System_out(?o) &*& o != null &*&
		    [_]ProbeInv(this) &*&
		    [_]TimeUnit_SECONDS(?s) &*& s != null;
		@*/
		{
			valueProduced = r.nextInt(sensor.max - sensor.min) + sensor.min;
			TimeUnit.SECONDS.sleep(2);
			System.out.println("Value Produced: " + Integer.toString(valueProduced));
		}
	}
}
	
	
	
	
	
	
	
	