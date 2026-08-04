import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  cart: [],

  //   cart: [
  //     {
  //       pizzaId: 12,
  //       meme: 'meditarrean',
  //       quantity: 4,
  //       unitPrice: 16,
  //       totalPrice: 32,
  //     },
  //   ],
};

const cartSlice = createSlice({
  name: 'cart',
  initialState,
  reducers: {
    addItem(state, action) {
      //payload = newItem
      state.cart.push(action.payload);
    },
    deleteItem(state, action) {
      // payload = pizza
      state.cart = state.cart.filter((item) => item.pizzaId !== action.payload);
    },
    increaseItemQuantity(state, action) {
      const item = state.cart.find((item) => item.pizzaId === action.payload);
      if (item) {
        item.quantity++;
        item.totalPrice = item.quantity * item.unitPrice;
      }
    },
    decreaseItemQuantity(state, action) {
      const item = state.cart.find((item) => item.pizzaId === action.payload);
      if (item) {
        item.quantity--;
        item.totalPrice = item.quantity * item.unitPrice;
      }
    },
    clearCart(state) {
      state.cart = [];
    },
  },
});

export const {
  addItem,
  deleteItem,
  increaseItemQuantity,
  decreaseItemQuantity,
  clearCart,
} = cartSlice.actions;

export default cartSlice.reducer;

export const getCart = (state) => state.cart.cart;

export const getTotalCartQuantity = (state) =>
  state.cart.cart.reduce((sum, item) => sum + item.quantity, 0);

export const getTotalCartPrice = (state) =>
  state.cart.cart.reduce((sum, item) => sum + item.totalPrice, 0);

// import { createSlice } from '@reduxjs/toolkit';
// import { createSelector } from 'reselect';

// const initialState = {
//   cart: [],

//   //   cart: [
//   //     {
//   //       pizzaId: 12,
//   //       meme: 'meditarrean',
//   //       quantity: 4,
//   //       unitPrice: 16,
//   //       totalPrice: 32,
//   //     },
//   //   ],
// };

// const cartSlice = createSlice({
//   name: 'cart',
//   initialState,
//   reducers: {
//     addItem(state, action) {
//       //payload = newItem
//       state.cart.push(action.payload);
//     },
//     deleteItem(state, action) {
//       // payload = pizza
//       state.cart = state.cart.filter((item) => item.pizzaId !== action.payload);
//     },
//     increaseItemQuantity(state, action) {
//       const item = state.cart.find((item) => item.pizzaId === action.payload);
//       if (item) {
//         item.quantity++;
//         item.totalPrice = item.quantity * item.unitPrice;
//       }
//     },
//     decreaseItemQuantity(state, action) {
//       const item = state.cart.find((item) => item.pizzaId === action.payload);
//       if (item) {
//         item.quantity--;
//         item.totalPrice = item.quantity * item.unitPrice;
//       }
//     },
//     clearCart(state) {
//       state.cart = [];
//     },
//   },
// });

// export const {
//   addItem,
//   deleteItem,
//   increaseItemQuantity,
//   decreaseItemQuantity,
//   clearCart,
// } = cartSlice.actions;

// export default cartSlice.reducer;

// export const getCart = (state) => state.cart.cart;

// export const getTotalCartQuantity = createSelector(
//   (state) => state.cart.cart,
//   (cart) => cart.reduce((sum, item) => sum + item.quantity, 0),
// );

// export const getTotalCartPrice = createSelector(
//   (state) => state.cart.cart,
//   (cart) => cart.reduce((sum, item) => sum + item.totalPrice, 0),
// );
