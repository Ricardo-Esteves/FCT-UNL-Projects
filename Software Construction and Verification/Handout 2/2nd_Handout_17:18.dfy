//Ricardo Esteves Nº 44930 
  
class Person {
    var bd:DataBase?;
    var id: int;
    var age: int;
    var name: string;
    var gender: string;

    function RepInv():bool
        reads this

    { id >= -1}

    //Invalid ID && Fail conection 
    function Transient():bool
        reads this
    { 
        RepInv() && id == -1 && bd == null
    }

    //Valid ID && Conection Valid
    function Persistent():bool
        reads this, this.bd
    { 
        RepInv() && id != -1 && bd != null && bd.RepInv()
    }

    //Valid ID && Fail Conection 
    function Detached():bool
        reads this
    { 
        RepInv() && id != -1 && bd == null
    }

    constructor(id:int)

        ensures Transient()
    {
        bd := null;
        this.id := -1;
    }

    //Delete a Person from DataBase
    method delete(index:int)

        modifies this`bd, this`id, bd`size,bd.collection
        requires Persistent() && bd.RepInv() && index > 0
        ensures Transient() 
    {
        bd.Delete(index);
        this.id := -1;
        this.bd := null;
    }

     method save(bd:DataBase)
        modifies this`bd, this`id, bd`size, bd.collection
        requires Transient() && bd.RepInv()
        ensures Persistent() && bd.RepInv()
        ensures bd.collection == old (bd.collection)
        ensures this.bd.collection == old (bd.collection)
    {  
        this.bd := bd;      
        this.id := bd.size;
        bd.Save(this);
    }

    //Open connection to DataBase
    method update(bd:DataBase)
        modifies this`bd
        requires Detached() && bd.RepInv()
        ensures Persistent() && bd.RepInv()
    {
        this.bd := bd;
    }
    //close connection to DataBase
    method close()
        modifies this`bd
        requires Persistent()
        ensures Detached()
    {
        this.bd := null;
    }

}

class DataBase {
    var collection:array<Person?>;
    var size:int;

    function RepInv():bool
        reads this`size,this`collection
    { 0 <= this.size < collection.Length }


    constructor ()
        ensures RepInv()
        ensures fresh(collection)
    {
        collection := new Person?[10];
        size := 0;
    }

    //Delete a person from DataBase
    method Delete(id:int)
        modifies collection, this`size
        requires RepInv() 
        ensures RepInv()
    {       
        if( 0 <= id < collection.Length && this.size > 0) {

            collection[id] := null;
            this.size := this.size - 1;
        }
    }

    //Add a person to the DataBase
    method Save(p:Person)
        modifies collection, this`size
        requires RepInv() && this.size < collection.Length
        ensures RepInv() 
    {
        if( 0 <= this.size < collection.Length - 1 ) {

            collection[this.size] := new Person(this.size);
            this.size := this.size + 1;
        }
    }

    //Return the person with the given id
     method Find(id: int) returns (p: Person?)

        requires 0 <= id < collection.Length && RepInv() 
        ensures RepInv()
    {
        return collection[id];
    }
}