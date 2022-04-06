class Customer extends Account{
    constructor(myGame, wishList, customer_id, transaksi){
        this.myGame = myGame;
        this.wishList = wishList;
        this.customer_id = customer_id;
        this.transaksi = transaksi;
    }

    buyGame(){};
    addToWishList(){};
    deleteWishList(){};
    viewMyGame(){};
    viewTransaksi(){};
}