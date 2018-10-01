//Ricardo Esteves Nº 44930

function unique(a:array<int>, n:int):bool
    requires a != null
    requires 0 <= n <= a.Length
    reads a
{ 
    forall i :: (0 <= i < n) ==> forall j :: (i < j < n) ==> a[i] != a[j]
}
function sorted(a:array<int>, n:int):bool
    requires a != null
    requires 0 <= n <= a.Length
    reads a
{ 
    forall i :: (0 <= i < n) ==> forall j :: (i < j < n) ==> a[i] <= a[j]
}

function contains(b:array<int>, m:int, v:int):bool
    requires b != null
    requires 0 <= m <= b.Length 
    reads b
{
    // exists l :: 0 <= l < m && b[l] == v
    v in b[..m]
}

// the method eliminates the duplicates in an array.
// a -> array with duplicates
// n -> number of elements in array a
// b -> array without duplicates
// m -> number of elements no array b
method Deduplicate(a:array<int>, n:int) returns (b:array<int>, m:int)
    requires a != null
    requires 0 <= n <= a.Length
    requires sorted(a,n)
    ensures b != null
    ensures 0 <= m <= b.Length
    ensures sorted(b,m) && unique(b,m)
    ensures forall k :: (0 <= k < n) && contains(b,m,a[k]) ==> contains(a,n,a[k])
  
{
    //Array b initialization
    b := new int[n];
    
    //Base Case (No elements in array a)
    if (n == 0) {return b,0;}

    //First element into array b
    var i := 1;
    b[0] := a[0];
    m := 1;
    

    while ( i < n)

        decreases n - i 
        invariant 1 <= i <= n
        invariant 1 <= m <= i
        invariant sorted(b,m) && unique(b,m) 
        invariant forall k :: (0 <= k < i) && contains(b,m,a[k]) ==> contains(a,n,a[k])

    {
        
        if (a[i] > b[m-1]) {

            b[m] := a[i];
            
            m := m + 1;
            
        }
        
        i := i+1;

    }
    return b,m;
}