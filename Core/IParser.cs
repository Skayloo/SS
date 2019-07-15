using AngleSharp.Html.Dom;

namespace Piesa.Core
{
    interface IParser<T> where T : class
    {
        T Parse(IHtmlDocument document);
    }
}
