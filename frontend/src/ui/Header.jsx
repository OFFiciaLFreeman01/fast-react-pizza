import { Link } from 'react-router-dom';
import SearchOrder from '../features/order/SearchOrder';
import Username from '../features/user/Username';

function Header() {
  return (
    <header className="flex items-center justify-between bg-yellow-400 px-4 py-3 font-serif uppercase sm:px-6">
      <Link to="/" className="border-b border-stone-200 tracking-widest">
        Fast React Pizza Co.
      </Link>

      <SearchOrder />
      <Link to="/kitchen" className="text-sm tracking-normal normal-case text-stone-700">
        Kitchen
      </Link>
      <Username />
    </header>
  );
}

export default Header;
